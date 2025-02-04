"""
URL validation and platform detection utilities.
"""
import re
from typing import Optional
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """Check if a URL is valid.
    
    Args:
        url: The URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_platform(url: str) -> Optional[str]:
    """Detect the platform from a video URL.
    
    Args:
        url: The video URL
        
    Returns:
        Optional[str]: Platform name if detected, None otherwise
    """
    if not is_valid_url(url):
        return None
        
    # Common video platforms and their URL patterns
    platforms = {
        'youtube': r'(?:youtube\.com|youtu\.be)',
        'vimeo': r'vimeo\.com',
        'dailymotion': r'dailymotion\.com',
        'facebook': r'facebook\.com',
        'twitter': r'twitter\.com',
        'instagram': r'instagram\.com',
        'tiktok': r'tiktok\.com'
    }
    
    domain = urlparse(url).netloc.lower()
    
    for platform, pattern in platforms.items():
        if re.search(pattern, domain):
            return platform
            
    return None

def get_supported_platforms() -> list[str]:
    """Get a list of supported video platforms.
    
    Returns:
        list[str]: List of supported platform names
    """
    return [
        'YouTube',
        'Vimeo',
        'Dailymotion',
        'Facebook',
        'Twitter',
        'Instagram',
        'TikTok',
        'And many more...'
    ]
