from typing import Dict, Type
from services.interfaces import SocialMediaPublisher
from services.publishers import LinkedInPublisher, TwitterPublisher, InstagramPublisher, YouTubePublisher
from config.settings import SOCIAL_MEDIA_CONFIG

class PublisherFactory:
    """Factory class for creating social media publishers"""
    
    _publishers: Dict[str, Type[SocialMediaPublisher]] = {
        'linkedin': LinkedInPublisher,
        'twitter': TwitterPublisher,
        'instagram': InstagramPublisher,
        'youtube': YouTubePublisher
    }
    
    @classmethod
    def create(cls, platform: str) -> SocialMediaPublisher:
        """Create a publisher instance for the specified platform"""
        if platform not in cls._publishers:
            raise ValueError(f"Unsupported platform: {platform}")
            
        publisher_class = cls._publishers[platform]
        config = SOCIAL_MEDIA_CONFIG.get(platform, {})
        return publisher_class(config)
