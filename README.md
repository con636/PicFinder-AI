# PicFinder AI 🔍

<div align="center">
  <img src="public/logo.png" width="100" alt="PicFinder Logo">
  <h3>Smart Local Image Search</h3>
</div>

**PicFinder AI** is a desktop app that lets you search your local photos using natural language descriptions. Powered by **OpenAI CLIP** and **FastAPI**, running entirely offline.

## 🛠️ Setup & Run

### 1. Python Backend
First, set up the AI server.

```bash
# Create virtual env
python -m venv venv
# Activate (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
cd backend
uvicorn server:app --reload --port 8000