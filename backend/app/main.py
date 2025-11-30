import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from pathlib import Path

from app.services.downloader import downloader

app = FastAPI(
    title="TikTok Video Downloader",
    description="API for downloading TikTok videos",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DownloadRequest(BaseModel):
    url: str


class VideoInfo(BaseModel):
    title: str
    duration: int
    thumbnail: str
    uploader: str
    view_count: int


class DownloadResponse(BaseModel):
    success: bool
    filename: str
    title: str
    duration: int
    download_url: str


@app.get("/")
async def root():
    return {"message": "TikTok Video Downloader API", "status": "running"}


@app.post("/api/info")
async def get_video_info(request: DownloadRequest):
    """Get video information without downloading"""
    try:
        # Validate TikTok URL
        if "tiktok.com" not in request.url.lower():
            raise HTTPException(status_code=400, detail="Please provide a valid TikTok URL")
        
        info = downloader.get_video_info(request.url)
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/download", response_model=DownloadResponse)
async def download_video(request: DownloadRequest):
    """Download a TikTok video"""
    try:
        # Validate TikTok URL
        if "tiktok.com" not in request.url.lower():
            raise HTTPException(status_code=400, detail="Please provide a valid TikTok URL")
        
        result = downloader.download_video(request.url)
        
        return DownloadResponse(
            success=True,
            filename=result['filename'],
            title=result['title'],
            duration=result['duration'],
            download_url=f"/api/file/{result['filename']}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def remove_file_background(filepath: str):
    """Background task to remove file after serving"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass


@app.get("/api/file/{filename}")
async def serve_file(filename: str, background_tasks: BackgroundTasks):
    """Serve the downloaded video file"""
    filepath = downloader.downloads_dir / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Schedule file cleanup after 5 minutes (optional - commented out for now)
    # background_tasks.add_task(remove_file_background, str(filepath))
    
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="video/mp4",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


@app.delete("/api/file/{filename}")
async def delete_file(filename: str):
    """Delete a downloaded file"""
    success = downloader.cleanup_file(filename)
    if success:
        return {"message": "File deleted successfully"}
    raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
