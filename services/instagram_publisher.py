import os
from typing import Optional
import requests
from datetime import datetime
import json

class InstagramPublisher:
    def __init__(self):
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.api_version = 'v18.0'  # Latest version as of now
        self.base_url = f'https://graph.facebook.com/{self.api_version}'

    def verify_credentials(self) -> bool:
        """Verify if the access token is valid."""
        try:
            url = f'{self.base_url}/me'
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params)
            return response.status_code == 200
        except Exception as e:
            print(f"Error verifying credentials: {str(e)}")
            return False

    def upload_media(self, media_path: str) -> Optional[str]:
        """Upload media to Instagram and get the media ID."""
        try:
            # First, create a container for the media
            url = f'{self.base_url}/{self.account_id}/media'
            
            params = {
                'access_token': self.access_token,
                'caption': 'Post created via API',
                'image_url': media_path  # Instagram accepts URLs, so media should be publicly accessible
            }

            response = requests.post(url, params=params)
            if response.status_code != 200:
                print(f"Error uploading media: {response.text}")
                return None

            creation_id = response.json().get('id')
            return creation_id

        except Exception as e:
            print(f"Error in upload_media: {str(e)}")
            return None

    def publish_post(self, caption: str, media_id: Optional[str] = None) -> bool:
        """Publish a post to Instagram."""
        try:
            url = f'{self.base_url}/{self.account_id}/media_publish'
            
            params = {
                'access_token': self.access_token,
                'creation_id': media_id
            }

            response = requests.post(url, params=params)
            if response.status_code != 200:
                print(f"Error publishing post: {response.text}")
                return False

            return True

        except Exception as e:
            print(f"Error in publish_post: {str(e)}")
            return False

    def create_post(self, caption: str, media_path: Optional[str] = None) -> bool:
        """Create a complete Instagram post with media."""
        try:
            if not self.verify_credentials():
                print("Invalid or expired credentials")
                return False

            if not media_path:
                print("Instagram requires media for posts")
                return False

            # Upload media
            media_id = self.upload_media(media_path)
            if not media_id:
                return False

            # Publish the post
            return self.publish_post(caption, media_id)

        except Exception as e:
            print(f"Error creating post: {str(e)}")
            return False
