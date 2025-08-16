from services.instagram_publisher import InstagramPublisher
import os
from datetime import datetime

def test_instagram_posting():
    # Initialize the Instagram publisher
    instagram = InstagramPublisher()
    
    # First, verify credentials
    print("Verifying credentials...")
    if not instagram.verify_credentials():
        print("❌ Credential verification failed!")
        return False
    print("✅ Credentials verified successfully!")
    
    # Test with a sample image from the media folder
    test_image_path = "https://raw.githubusercontent.com/Abhiroop-hgv/YuktiManthan---AI-media-content-generator/main/media/20250815_012720_7e698106afc8897c27ba04400c906d59.jpg"
    test_caption = f"Test post from YuktiManthan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    print("Attempting to create post...")
    result = instagram.create_post(caption=test_caption, media_path=test_image_path)
    
    if result:
        print("✅ Post created successfully!")
    else:
        print("❌ Failed to create post!")
    
    return result

if __name__ == "__main__":
    test_instagram_posting()
