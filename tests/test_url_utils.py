"""
Tests for URL validation and platform detection utilities.
"""
import pytest
from src.utils.url_utils import is_valid_url, get_platform

def test_is_valid_url():
    """Test URL validation."""
    # Valid URLs
    assert is_valid_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert is_valid_url("https://youtu.be/dQw4w9WgXcQ")
    assert is_valid_url("https://vimeo.com/123456789")
    
    # Invalid URLs
    assert not is_valid_url("")
    assert not is_valid_url("not a url")
    assert not is_valid_url("http://")
    assert not is_valid_url("youtube.com")  # Missing scheme

def test_get_platform():
    """Test platform detection."""
    # YouTube
    assert get_platform("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "youtube"
    assert get_platform("https://youtu.be/dQw4w9WgXcQ") == "youtube"
    
    # Vimeo
    assert get_platform("https://vimeo.com/123456789") == "vimeo"
    
    # Dailymotion
    assert get_platform("https://www.dailymotion.com/video/x7tgd2g") == "dailymotion"
    
    # Facebook
    assert get_platform("https://www.facebook.com/watch?v=123456789") == "facebook"
    
    # Twitter
    assert get_platform("https://twitter.com/user/status/123456789") == "twitter"
    
    # Instagram
    assert get_platform("https://www.instagram.com/p/ABC123/") == "instagram"
    
    # TikTok
    assert get_platform("https://www.tiktok.com/@user/video/123456789") == "tiktok"
    
    # Unknown/Invalid
    assert get_platform("https://example.com/video") is None
    assert get_platform("not a url") is None
    assert get_platform("") is None
