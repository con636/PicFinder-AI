import os
import shutil
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from sentence_transformers import SentenceTransformer, util
from deep_translator import GoogleTranslator
import chromadb
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse # <--- 新增这个

import sys
import subprocess
import platform
# ================= 配置与初始化 =================
app = FastAPI(title="LocalLens Backend")

# 允许跨域 (CORS)，这样 Electron/Vue 才能访问 Python 后端
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库路径
DB_PATH = "./db/chroma_db"
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(
    name="photos", 
    metadata={"hnsw:space": "cosine"} # <--- 关键修改
)

# 全局模型变量
model = None


@app.on_event("startup")
def load_model():
    """服务器启动时加载模型，只需加载一次"""
    global model
    print("⏳ 正在加载 AI 模型 (clip-ViT-L-14)...")
    model = SentenceTransformer('clip-ViT-L-14')
    print("✅ 模型加载完毕！引擎已就绪。")


# ================= 数据结构定义 =================
class ScanRequest(BaseModel):
    folder_path: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 20


# ================= 辅助函数 =================
def translate_to_english(text):
    try:
        # 如果是纯英文，直接返回，省时间
        if all(ord(c) < 128 for c in text):
            return text
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text


# ================= API 接口 =================

@app.get("/")
def health_check():
    return {"status": "running", "model": "clip-ViT-L-14"}


@app.post("/scan")
def scan_images(request: ScanRequest):
    """扫描指定文件夹建立索引"""
    folder_path = request.folder_path
    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="文件夹不存在")

    print(f"📂 开始扫描: {folder_path}")
    image_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                image_paths.append(os.path.join(root, file))

    # 增量更新检查
    existing = collection.get(ids=image_paths, include=[])
    existing_ids = set(existing['ids'])
    new_paths = [p for p in image_paths if p not in existing_ids]

    if not new_paths:
        return {
            "message": "所有图片已是最新",
            "total_scanned": len(image_paths),  # 补上这个字段
            "new_indexed": 0  # 把 new_count 改名为 new_indexed
        }

    # 批量处理
    batch_size = 16
    processed_count = 0

    for i in range(0, len(new_paths), batch_size):
        batch = new_paths[i: i + batch_size]
        try:
            images = [Image.open(p) for p in batch]
            embeddings = model.encode(images)

            collection.add(
                embeddings=embeddings.tolist(),
                documents=batch,  # 存路径作为文档内容
                ids=batch
            )
            processed_count += len(batch)
            print(f"   -> 进度: {processed_count}/{len(new_paths)}")
        except Exception as e:
            print(f"⚠️ 批次处理出错: {e}")

    return {
        "message": "扫描完成",
        "total_scanned": len(image_paths),
        "new_indexed": processed_count
    }


@app.post("/search")
def search_images(request: SearchRequest):
    """语义搜索接口"""
    # 1. 翻译
    english_query = translate_to_english(request.query)
    print(f"🔍 搜索: {request.query} -> {english_query}")

    # 2. 编码
    query_vec = model.encode([english_query]).tolist()

    # 3. 查询数据库
    results = collection.query(
        query_embeddings=query_vec,
        n_results=request.top_k,
        include=['documents', 'distances']
    )

    # 4. 格式化返回结果
    response_data = []
    if results['documents'][0]:
        for i, path in enumerate(results['documents'][0]):
            dist = results['distances'][0][i]
            score = max(0, (1 - dist) * 100)  # 简单分数换算

            response_data.append({
                "path": path,
                "filename": os.path.basename(path),
                "score": round(score, 1)
            })

    return {"results": response_data, "translated_query": english_query}

class OpenRequest(BaseModel):
    path: str

@app.get("/thumbnail")
def get_thumbnail(path: str):
    """
    前端给一个路径，后端返回图片文件流。
    这样前端就可以用 <img src="http://.../thumbnail?path=..."> 来显示图片了
    """
    if os.path.exists(path):
        # 实际生产中这里应该生成缩略图以加快速度，现在为了省事直接返回原图
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/open")
def open_image(request: OpenRequest):
    """跨平台打开图片"""
    try:
        path = request.path
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")

        system_name = platform.system()

        if system_name == 'Windows':
            os.startfile(path)
        elif system_name == 'Darwin':  # macOS
            subprocess.call(('open', path))
        else:  # Linux
            subprocess.call(('xdg-open', path))

        return {"status": "opened"}
    except Exception as e:
        print(f"打开文件失败: {e}")  # 打印错误日志
        raise HTTPException(status_code=500, detail=str(e))