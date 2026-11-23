from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
import re
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


def get_video_id(url):
    parsed = urlparse(str(url))
    host = (parsed.hostname or "").lower()

    if host in ["youtube.com", "www.youtube.com", "m.youtube.com"]:
        video_id = parse_qs(parsed.query).get("v", [None])[0]
    elif host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
    else:
        return None

    if video_id and len(video_id) == 11:
        return video_id

    return None


@app.get("/")
def home():
    return {"message": "CLIPORA AI Backend is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/video-info")
def video_info(request: VideoRequest):
    video_id = get_video_id(request.video_url)

    if not video_id:
        raise HTTPException(400, "Invalid YouTube video URL")

    oembed_url = (
        "https://www.youtube.com/oembed"
        f"?url=https://www.youtube.com/watch?v={video_id}&format=json"
    )

    try:
        with urlopen(oembed_url, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        iframe_html = str(data.get("html") or "")
        title_match = re.search(r'<iframe[^>]*\btitle="([^"]+)"', iframe_html)
        video_title = title_match.group(1) if title_match else "Title unavailable"
        return {
            "status": "success",
            "video_id": video_id,
            "title": str(video_title),
            "channel": data.get("author_name") or "Channel unavailable",
            "thumbnail": data.get("thumbnail_url") or None,
            "message": "Video information retrieved successfully."
    }

         except (HTTPError, URLError, TimeoutError):
        raise HTTPException(
            404,
            "Video information unavailable. Check the link and video visibility."
    )
        )


@app.post("/process")
def process_video(request: VideoRequest):
    video_id = get_video_id(request.video_url)

    if not video_id:
        raise HTTPException(400, "Please enter a valid YouTube URL")

    return {
        "status": "accepted",
        "video_id": video_id,
        "clip_length": request.clip_length,
        "language": request.language,
        "message": "Video link accepted. Processing engine is not ready yet."
    }
