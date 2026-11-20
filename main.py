from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="CLIPORA AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_url: HttpUrl
    clip_length: int = 60
    language: str = "English"

@app.get("/")
def home():
    return {
        "message": "CLIPORA AI Backend is running!",
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/process")
def process_video(request: VideoRequest):
    return {
        "status": "received",
        "video_url": str(request.video_url),
        "clip_length": request.clip_length,
        "language": request.language,
        "message": "Video request received. Processing engine is not installed yet."
    }
  
