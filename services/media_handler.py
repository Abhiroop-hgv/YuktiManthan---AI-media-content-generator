import os
from typing import List, Optional
from PIL import Image

class MediaHandler:
    """Handle media file operations."""
    
    def __init__(self, allowed_types: List[str], max_size: int):
        self.allowed_types = allowed_types
        self.max_size = max_size
    
    def validate_file(self, file_path: str) -> bool:
        """Validate file type and size."""
        if not os.path.exists(file_path):
            return False
            
        # Check file size
        if os.path.getsize(file_path) > self.max_size:
            return False
            
        # Check file type
        file_ext = file_path.split('.')[-1].lower()
        if file_ext not in self.allowed_types:
            return False
            
        return True
    
    def optimize_image(self, file_path: str, output_path: Optional[str] = None) -> str:
        """Optimize image for social media."""
        try:
            img = Image.open(file_path)
            
            # If output path not specified, create one
            if not output_path:
                filename = os.path.basename(file_path)
                output_path = f"optimized_{filename}"
            
            # Resize if too large
            max_size = (1920, 1080)  # Standard social media size
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(output_path, optimize=True, quality=85)
            
            return output_path
        except Exception as e:
            print(f"Error optimizing image: {str(e)}")
            return file_path
