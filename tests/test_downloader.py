"""
Tests for video downloader functionality.
"""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.downloader import VideoDownloader, VideoFormat, DownloadProgress

@pytest.fixture
def mock_progress_callback():
    """Fixture providing a mock progress callback."""
    return MagicMock()

@pytest.fixture
def temp_download_dir(tmp_path):
    """Fixture providing a temporary download directory."""
    return tmp_path / "downloads"

def test_video_downloader_initialization(mock_progress_callback, temp_download_dir):
    """Test VideoDownloader initialization."""
    downloader = VideoDownloader(mock_progress_callback, temp_download_dir)
    
    assert downloader.progress_callback == mock_progress_callback
    assert downloader.download_path == temp_download_dir
    assert temp_download_dir.exists()

def test_video_format_setting(mock_progress_callback, temp_download_dir):
    """Test setting video format."""
    downloader = VideoDownloader(mock_progress_callback, temp_download_dir)
    
    # Test each format
    for format in VideoFormat:
        downloader.set_format(format)
        assert downloader.ydl_opts['format'] == format.value

@patch('yt_dlp.YoutubeDL')
def test_successful_download(mock_ydl, mock_progress_callback, temp_download_dir):
    """Test successful video download."""
    downloader = VideoDownloader(mock_progress_callback, temp_download_dir)
    
    # Mock successful download
    mock_ydl.return_value.__enter__.return_value.download.return_value = 0
    
    result = downloader.download("https://www.youtube.com/watch?v=test")
    assert result is True

@patch('yt_dlp.YoutubeDL')
def test_failed_download(mock_ydl, mock_progress_callback, temp_download_dir):
    """Test failed video download."""
    downloader = VideoDownloader(mock_progress_callback, temp_download_dir)
    
    # Mock failed download
    mock_ydl.return_value.__enter__.return_value.download.side_effect = Exception("Download failed")
    
    result = downloader.download("https://www.youtube.com/watch?v=test")
    assert result is False
    
    # Verify error progress was reported
    mock_progress_callback.assert_called_with(
        DownloadProgress(
            status="error",
            percent=0.0,
            filename="Download failed"
        )
    )

def test_progress_hook(mock_progress_callback, temp_download_dir):
    """Test progress hook handling."""
    downloader = VideoDownloader(mock_progress_callback, temp_download_dir)
    
    # Test downloading progress
    downloader._progress_hook({
        'status': 'downloading',
        'percentage': 50.0,
        'speed_str': '1.0 MiB/s',
        'eta_str': '30s',
        'filename': 'test.mp4'
    })
    
    mock_progress_callback.assert_called_with(
        DownloadProgress(
            status="downloading",
            percent=50.0,
            speed="1.0 MiB/s",
            eta="30s",
            filename="test.mp4"
        )
    )
    
    # Test finished progress
    downloader._progress_hook({
        'status': 'finished',
        'filename': 'test.mp4'
    })
    
    mock_progress_callback.assert_called_with(
        DownloadProgress(
            status="finished",
            percent=100.0,
            filename="test.mp4"
        )
    )
