"""
Video downloader implementation using yt-dlp.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

import yt_dlp

class VideoFormat(Enum):
    """Video format options."""
    BEST = "best"
    HD = "best[height<=720]"
    SD = "best[height<=480]"
    AUDIO = "bestaudio"

@dataclass
class DownloadProgress:
    """Download progress information."""
    status: str
    percent: float
    speed: Optional[str] = None
    eta: Optional[str] = None
    filename: Optional[str] = None

class VideoDownloader:
    """Handles video downloads using yt-dlp."""
    
    def __init__(
        self,
        progress_callback: Callable[[DownloadProgress], None],
        download_path: Optional[Path] = None
    ):
        """Initialize the downloader.
        
        Args:
            progress_callback: Function to call with download progress updates
            download_path: Optional custom download directory
        """
        self.progress_callback = progress_callback
        self.download_path = download_path or Path.home() / "Downloads"
        self.download_path.mkdir(parents=True, exist_ok=True)
        
        # Configure yt-dlp options
        self.ydl_opts = {
            'format': VideoFormat.BEST.value,
            'progress_hooks': [self._progress_hook],
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'noprogress': False,  # Enable progress updates
        }
    
    def set_format(self, format: VideoFormat):
        """Set the video format for downloads.
        
        Args:
            format: The VideoFormat to use
        """
        self.ydl_opts['format'] = format.value
    
    def _progress_hook(self, d: dict):
        """Handle download progress updates from yt-dlp.
        
        Args:
            d: Progress information dictionary from yt-dlp
        """
        if d['status'] == 'downloading':
            # Calculate progress
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
            else:
                percent = d.get('percentage', 0)
                
            # Ensure percent is within bounds
            if percent > 100:
                percent = 100
            elif percent < 0:
                percent = 0
            
            # Create progress update
            progress = DownloadProgress(
                status="downloading",
                percent=percent,
                speed=d.get('speed_str'),
                eta=d.get('eta_str'),
                filename=d.get('filename')
            )
            
        elif d['status'] == 'finished':
            progress = DownloadProgress(
                status="finished",
                percent=100.0,
                filename=d.get('filename')
            )
            
        elif d['status'] == 'error':
            progress = DownloadProgress(
                status="error",
                percent=0.0,
                filename=d.get('filename')
            )
            
        else:
            return
            
        # Send progress update
        self.progress_callback(progress)
    
    def download(self, url: str) -> bool:
        """Download a video.
        
        Args:
            url: The video URL to download
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            return True
            
        except Exception as e:
            # Send error progress
            self.progress_callback(DownloadProgress(
                status="error",
                percent=0.0,
                filename=str(e)
            ))
            return False
