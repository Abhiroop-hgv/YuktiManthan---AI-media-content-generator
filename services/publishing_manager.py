from typing import Dict, Optional
from services.publishers import (
    LinkedInPublisher,
    TwitterPublisher,
    InstagramPublisher,
    YouTubePublisher
)
from services.media_handler import MediaHandler
from config.settings import ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE

class PublishingManager:
    """Manage social media publishing operations."""
    
    def __init__(self):
        self.publishers = {
            'linkedin': LinkedInPublisher(),
            'twitter': TwitterPublisher(),
            'instagram': InstagramPublisher(),
            'youtube': YouTubePublisher()
        }
        self.media_handler = MediaHandler(ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE)
    
    async def initialize_publishers(self) -> Dict[str, bool]:
        """Initialize and authenticate all publishers."""
        auth_status = {}
        for platform, publisher in self.publishers.items():
            auth_status[platform] = await publisher.authenticate()
        return auth_status
    
    async def publish_content(self, 
                            platform: str, 
                            content: str, 
                            media_path: Optional[str] = None) -> dict:
        """Publish content to specified platform."""
        try:
            publisher = self.publishers.get(platform.lower())
            if not publisher:
                return {"success": False, "error": "Platform not supported"}
            
            # Validate and optimize media if provided
            if media_path:
                if not self.media_handler.validate_file(media_path):
                    return {"success": False, "error": "Invalid media file"}
                media_path = self.media_handler.optimize_image(media_path)
            
            # Publish content
            result = await publisher.publish_post(content, media_path)
            return {"success": True, "result": result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
