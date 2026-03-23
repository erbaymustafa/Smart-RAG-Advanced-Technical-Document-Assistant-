import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import warnings
import uvicorn
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from processor import process_document
from rag_chain import get_answer

warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Uygulama Durumu ve Log Dosyası
LOG_FILE = "feedback_logs.json"
app.state.extracted_text = ""
app.state.chat_history = [] # [{"id": 0, "q": "...", "a": "...", "feedback": None}]

@app.get("/")
async def index(request: Request):
    # Context sözlüğünü ayrı bir değişkende tanımlayıp gönderiyoruz
    context = {
        "request": request, 
        "chat_history": app.state.chat_history,
        "extracted_text": app.state.extracted_text
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        app.state.extracted_text = process_document(file)
        app.state.chat_history = [] 
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": f"Hata: {str(e)}"})

@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    if not app.state.extracted_text:
        return RedirectResponse(url="/", status_code=303)
    
    try:
        # Önbellek Kontrolü
        for chat in app.state.chat_history:
            if chat['q'].strip().lower() == question.strip().lower():
                return RedirectResponse(url="/", status_code=303)

        answer = get_answer(app.state.extracted_text, question)
        new_chat = {
            "id": len(app.state.chat_history), 
            "q": question, 
            "a": answer,
            "feedback": None
        }
        app.state.chat_history.append(new_chat)
        return RedirectResponse(url="/", status_code=303)
    except Exception:
        return RedirectResponse(url="/", status_code=303)

@app.post("/feedback/{chat_id}/{status}")
async def save_feedback(chat_id: int, status: str):
    if 0 <= chat_id < len(app.state.chat_history):
        chat_item = app.state.chat_history[chat_id]
        chat_item["feedback"] = status
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": chat_item["q"],
            "answer": chat_item["a"],
            "status": status
        }

        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try: logs = json.load(f)
                except: logs = []

        # Mükerrer Kontrolü ve Güncelleme
        found = False
        for entry in logs:
            if entry["question"] == log_entry["question"] and entry["answer"] == log_entry["answer"]:
                entry["status"] = status
                entry["timestamp"] = log_entry["timestamp"]
                found = True
                break
        
        if not found:
            logs.append(log_entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
