import os
import sys
from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal
import yt_dlp

class VideoDownloader(QObject):
    progress = pyqtSignal(float, str)
    error = pyqtSignal(str)
    complete = pyqtSignal(str)  # Now emits the filename

    def __init__(self):
        super().__init__()
        self.ydl_opts = None
        self._setup_ffmpeg_path()

    def _setup_ffmpeg_path(self):
        """Set up ffmpeg path to use bundled binaries."""
        if getattr(sys, 'frozen', False):
            # Running in a bundle
            bundle_dir = sys._MEIPASS
            ffmpeg_path = os.path.join(bundle_dir, 'ffmpeg.exe')
            ffprobe_path = os.path.join(bundle_dir, 'ffprobe.exe')
            if os.path.exists(ffmpeg_path) and os.path.exists(ffprobe_path):
                os.environ["PATH"] = f"{bundle_dir};{os.environ['PATH']}"

    def _progress_hook(self, d: Dict[str, Any]) -> None:
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%', '')
            try:
                percentage = float(p)
                self.progress.emit(percentage, 'Downloading...')
            except ValueError:
                self.progress.emit(0, 'Starting download...')
        elif d['status'] == 'finished':
            self.progress.emit(100, 'Download complete!')
            # Store the filename for later use
            self.last_filename = os.path.basename(d['filename'])

    def download(self, url: str, output_path: str, format_selection: str = 'best') -> None:
        """
        Download video from URL.
        
        Args:
            url: Video URL
            output_path: Output directory
            format_selection: Format to download ('best', 'hd', 'sd', 'audio')
        """
        format_opts = {
            'best': 'best',
            'hd': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'sd': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
            'audio': 'bestaudio/best'
        }

        self.ydl_opts = {
            'format': format_opts.get(format_selection, 'best'),
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': os.path.join(sys._MEIPASS, 'ffmpeg.exe') if getattr(sys, 'frozen', False) else None
        }

        try:
            # Initialize the filename
            self.last_filename = ""
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Get video info first to get the title
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')
                if format_selection == 'audio':
                    ext = 'mp3'
                
                # If we couldn't get the filename from the progress hook
                if not hasattr(self, 'last_filename') or not self.last_filename:
                    self.last_filename = f"{title}.{ext}"
                
                # Download the video
                ydl.download([url])
                
            # Emit the complete signal with the filename
            self.complete.emit(self.last_filename)
        except Exception as e:
            self.error.emit(str(e))

    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information without downloading."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            self.error.emit(str(e))
            return None
