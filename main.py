
from fastapi import FastAPI

app = FastAPI(title="CLIPORA AI")

@app.get("/")
def home():
    return {
        "message": "CLIPORA AI Backend is running!",
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
  
