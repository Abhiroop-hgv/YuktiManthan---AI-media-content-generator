from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class PublishingResult:
    """Data class for publishing results"""
    success: bool
    platform: str
    post_id: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class ContentGenerator(ABC):
    """Abstract base class for content generation"""
    @abstractmethod
    async def generate(self, prompt: str, target_language: str) -> Dict[str, str]:
        """Generate content for different platforms"""
        pass

class MediaHandler(ABC):
    """Abstract base class for media handling"""
    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """Validate media file"""
        pass

    @abstractmethod
    def process(self, file_path: str) -> str:
        """Process media file and return processed file path"""
        pass

class SocialMediaPublisher(ABC):
    """Abstract base class for social media publishing"""
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the platform"""
        pass

    @abstractmethod
    async def publish(self, content: str, media_path: Optional[str] = None) -> PublishingResult:
        """Publish content to the platform"""
        pass

    @abstractmethod
    def validate_content(self, content: str) -> bool:
        """Validate content for the platform"""
        pass

class Analytics(ABC):
    """Abstract base class for analytics"""
    @abstractmethod
    async def track_post(self, platform: str, post_id: str) -> None:
        """Track a post's performance"""
        pass

    @abstractmethod
    async def get_metrics(self, post_id: str) -> Dict[str, Any]:
        """Get metrics for a post"""
        pass
