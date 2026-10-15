# WoodCraft Furniture FAQ Assistant — Deployment Guide

## 1. Local setup

```bash
git clone https://github.com/muhammadadeel-se/woodcraft-faq-pipeline.git
cd woodcraft-faq-pipeline
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python build_index.py
```

## 2. Run locally

```bash
python app.py
```

Then open http://127.0.0.1:8080/chat

## 3. Validate the app

```bash
python -m pytest -q
```

## 4. Deploy to a web host

This project is configured for Gunicorn with a Procfile:

```text
web: gunicorn app:app
```

### PythonAnywhere

1. Upload the repo to your PythonAnywhere account.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   python build_index.py
   ```
3. Set the app entry to `app:app`.
4. Start the web app using Gunicorn.

### Render / Heroku-style hosts

1. Set the runtime command to:
   ```bash
   gunicorn app:app
   ```
2. Ensure the environment has the required Python version and dependency install step.
3. Make sure `faq.db`, `faiss_index.bin`, and `faq_ids.pkl` are present in the deployed project root.

## 5. Optional environment variables

```bash
export OPENAI_API_KEY="your-key"
export HUGGINGFACE_API_KEY="your-key"
```

These are optional. Without them, the app falls back to the local FAQ answer path for offline operation.