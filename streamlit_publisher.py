import streamlit as st
import asyncio
from typing import Optional
import os
from datetime import datetime
from services.publishing_manager import PublishingManager

class StreamlitPublisher:
    """Handle Streamlit UI for social media publishing."""
    
    def __init__(self):
        self.publishing_manager = PublishingManager()
        
    async def initialize(self):
        """Initialize publishers and check authentication status."""
        auth_status = await self.publishing_manager.initialize_publishers()
        return auth_status
    
    def save_uploaded_file(self, uploaded_file) -> Optional[str]:
        """Save uploaded file and return the file path."""
        if uploaded_file is None:
            return None
            
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"uploads/{timestamp}_{uploaded_file.name}"
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path
    
    async def publish_to_platform(self, platform: str, content: str, media_path: Optional[str] = None):
        """Publish content to specified platform."""
        result = await self.publishing_manager.publish_content(platform, content, media_path)
        return result
