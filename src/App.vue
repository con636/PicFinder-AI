<template>
  <div style="padding: 20px; font-family: 'Segoe UI', Roboto, sans-serif; color: #333;">
    
    <div style="display: flex; align-items: center; margin-bottom: 25px;">
      
      <img src="/logo.png" style="width: 60px; height: 60px; object-fit: contain; margin-right: 15px; border-radius: 8px;" />
      
      <div style="display: flex; flex-direction: column; justify-content: center; line-height: 1.2;">
        
        <div style="font-size: 24px; font-weight: 700; color: #2c3e50; letter-spacing: 0.5px;">
          PicFinder <span style="color: #007bff;">AI</span>
        </div>
        
        <div style="font-size: 13px; font-weight: 500; color: #666;">
          Smart Lens & Local Search
        </div>
        
      </div>
    </div>

    <div style="margin-bottom: 10px; display: flex; gap: 10px; align-items: center;">
      <select v-model="currentLang" style="padding: 8px; border-radius: 6px; border: 1px solid #ccc; background: white; cursor: pointer;">
        <option value="zh">中文</option>
        <option value="ja">日本語</option>
        <option value="en">English</option>
      </select>

      <button @click="selectFolder" style="padding: 8px 15px; background-color: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 6px; font-weight: 500;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
        </svg>
        {{ t('selectFolder') }}
      </button>

      <input 
        type="text" 
        v-model="folderPath" 
        readonly 
        style="flex: 1; padding: 8px 12px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; color: #495057;"
      />

      <button 
        @click="scanFolder" 
        :disabled="scanning" 
        :style="`padding: 8px 20px; background-color: ${scanning ? '#ccc' : '#28a745'}; color: white; border: none; border-radius: 6px; cursor: ${scanning ? 'not-allowed' : 'pointer'}; display: flex; align-items: center; gap: 6px; font-weight: 500; transition: background 0.2s;`"
      >
        <svg v-if="!scanning" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
        </svg>
        <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="spin">
          <line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
        </svg>
        {{ scanning ? t('scanning') : t('startScan') }}
      </button>
    </div>

    <div v-if="scanMsg" style="margin-bottom: 10px; color: #0056b3; font-size: 14px; font-weight: 500;">
      {{ scanMsg }}
    </div>

    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">

    <div style="margin-bottom: 20px; display: flex; gap: 10px;">
      <input 
        type="text" 
        v-model="query" 
        @keyup.enter="search" 
        :placeholder="t('searchPlaceholder')" 
        style="flex: 1; padding: 10px 15px; font-size: 16px; border: 1px solid #ced4da; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); outline: none;"
        onfocus="this.style.borderColor='#80bdff'; this.style.boxShadow='0 0 0 0.2rem rgba(0,123,255,.25)'"
        onblur="this.style.borderColor='#ced4da'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'"
      />
      <button @click="search" style="padding: 10px 25px; font-size: 16px; background-color: #0069d9; color: white; border: none; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        {{ t('searchBtn') }}
      </button>
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 15px;">
      <div 
        v-for="(item, index) in results" 
        :key="index" 
        @click="openImage(item.path)"
        style="width: 150px; cursor: pointer; border: 1px solid #eaeaea; border-radius: 8px; padding: 8px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s;"
        onmouseover="this.style.transform='translateY(-2px)'"
        onmouseout="this.style.transform='translateY(0)'"
      >
        <img 
          :src="`${API_URL}/thumbnail?path=${encodeURIComponent(item.path)}`" 
          style="width: 100%; height: 150px; object-fit: cover; display: block; border-radius: 4px;"
        />
        <div style="font-size: 12px; margin-top: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #555;">
          <span style="font-weight: bold; color: #28a745;">{{ item.score }}%</span> 
          {{ item.filename }}
        </div>
      </div>
    </div>

    <div v-if="results.length === 0 && searched" style="color: #6c757d; margin-top: 20px; text-align: center;">
      {{ t('noResults') }}
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue' // 引入 onMounted
import axios from 'axios'
const { ipcRenderer } = window.require('electron')
const API_URL = 'http://127.0.0.1:8000'

// 启动时设置窗口标题
onMounted(() => {
  document.title = 'PicFinder AI'
})

// --- 多语言配置 ---
const currentLang = ref('en')
const i18n = {
  zh: {
    selectFolder: '选择文件夹',
    startScan: '开始索引',
    scanning: '正在处理...',
    searchPlaceholder: '输入描述搜索图片...',
    searchBtn: '搜索',
    noResults: '未找到相关图片'
  },
  ja: {
    selectFolder: 'フォルダ選択',
    startScan: 'スキャン',
    scanning: '処理中...',
    searchPlaceholder: 'キーワードを入力...',
    searchBtn: '検索',
    noResults: '画像が見つかりません'
  },
  en: {
    selectFolder: 'Select Folder',
    startScan: 'Index',
    scanning: 'Indexing...',
    searchPlaceholder: 'Search keywords...',
    searchBtn: 'Search',
    noResults: 'No results found'
  }
}
const t = (key) => i18n[currentLang.value][key]

// --- 逻辑 ---
const folderPath = ref('')
const query = ref('')
const results = ref([])
const scanning = ref(false)
const scanMsg = ref('')
const searched = ref(false)

const selectFolder = async () => {
  const path = await ipcRenderer.invoke('dialog:openDirectory')
  if (path) folderPath.value = path
}

const scanFolder = async () => {
  if (!folderPath.value) return
  scanning.value = true
  scanMsg.value = 'Running...'
  try {
    const res = await axios.post(`${API_URL}/scan`, { folder_path: folderPath.value })
    scanMsg.value = `Done. Total: ${res.data.total_scanned}, New: ${res.data.new_indexed}`
  } catch (e) {
    scanMsg.value = 'Error.'
  }
  scanning.value = false
}

const search = async () => {
  if (!query.value) return
  searched.value = true
  try {
    const res = await axios.post(`${API_URL}/search`, { query: query.value, top_k: 50 })
    results.value = res.data.results
  } catch (e) {}
}

const openImage = async (path) => {
  try { await axios.post(`${API_URL}/open`, { path }) } catch (e) {}
}
</script>

<style>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.spin {
  animation: spin 1s linear infinite;
}
</style>