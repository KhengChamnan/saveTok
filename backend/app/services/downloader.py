import os
import uuid
import yt_dlp
from pathlib import Path

# Create downloads directory
DOWNLOADS_DIR = Path(__file__).parent.parent.parent / "downloads"
DOWNLOADS_DIR.mkdir(exist_ok=True)


class TikTokDownloader:
    """Service for downloading TikTok videos using yt-dlp"""
    
    def __init__(self):
        self.downloads_dir = DOWNLOADS_DIR
    
    def get_video_info(self, url: str) -> dict:
        """Extract video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'TikTok Video'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                }
            except Exception as e:
                raise Exception(f"Failed to extract video info: {str(e)}")
    
    def download_video(self, url: str) -> dict:
        """Download TikTok video and return file path"""
        # Generate unique filename
        video_id = str(uuid.uuid4())[:8]
        output_template = str(self.downloads_dir / f"{video_id}.%(ext)s")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            # TikTok specific options
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                
                # Find the downloaded file
                ext = info.get('ext', 'mp4')
                filename = f"{video_id}.{ext}"
                filepath = self.downloads_dir / filename
                
                if not filepath.exists():
                    # Try to find any file with the video_id prefix
                    for file in self.downloads_dir.glob(f"{video_id}.*"):
                        filepath = file
                        filename = file.name
                        break
                
                return {
                    'success': True,
                    'filename': filename,
                    'filepath': str(filepath),
                    'title': info.get('title', 'TikTok Video'),
                    'duration': info.get('duration', 0),
                }
            except Exception as e:
                raise Exception(f"Failed to download video: {str(e)}")
    
    def cleanup_file(self, filename: str) -> bool:
        """Remove a downloaded file"""
        filepath = self.downloads_dir / filename
        try:
            if filepath.exists():
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False


# Singleton instance
downloader = TikTokDownloader()
