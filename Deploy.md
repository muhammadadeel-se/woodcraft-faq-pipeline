# Deployment & Setup Documentation - WoodCraft FAQ RAG Pipeline

## Architecture Overview
* **Framework:** Flask (WSGI via Gunicorn)
* **Retrieval Engine:** FAISS Vector Index (`IndexFlatL2`)
* **Embedding Model:** `all-MiniLM-L6-v2` (SentenceTransformers)
* **LLM Completion:** OpenAI API integration (`OPENAI_API_KEY`)

## Production Deployment (Render)
This project is configured for cloud deployment on **Render** using a native Python Web Service defined in `render.yaml`.

### 1. Render Service Specifications
* **Service Type:** Web Service (`type: web`)
* **Environment:** Python 3 Native
* **Build Command:** 
  ```bash
  pip install torch --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu) && pip install -r requirements.txt