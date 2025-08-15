import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class InstagramPublisher:
    def __init__(self):
        load_dotenv()
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.api_version = 'v18.0'  # Meta API version
        self.base_url = f'https://graph.facebook.com/{self.api_version}'

    async def publish_post(self, caption: str, media_path: str) -> Dict[str, Any]:
        """
        Publish a post to Instagram with image and caption.
        
        Args:
            caption (str): The caption for the post
            media_path (str): Path to the image file
            
        Returns:
            dict: Response containing success status and post details
        """
        try:
            # Validate credentials
            if not self.access_token or not self.account_id:
                return {
                    'success': False,
                    'error': 'Missing Instagram credentials. Please check your .env file.',
                    'details': f'Account ID: {"Set" if self.account_id else "Missing"}, Access Token: {"Set" if self.access_token else "Missing"}'
                }

            # Validate media file
            if not os.path.exists(media_path):
                return {
                    'success': False,
                    'error': 'Media file not found',
                    'details': f'Could not find file at path: {media_path}'
                }

            print(f"Attempting to create media container... Account ID: {self.account_id}")
            # 1. Create container for the media
            container_response = self._create_media_container(media_path, caption)
            
            # Log the container response for debugging
            print(f"Container Response: {container_response}")
            
            if 'error' in container_response:
                return {
                    'success': False,
                    'error': 'Instagram API Error',
                    'details': container_response['error'].get('message', 'Unknown error'),
                    'error_type': container_response['error'].get('type', 'Unknown'),
                    'error_code': container_response['error'].get('code', 'Unknown')
                }

            if not container_response.get('id'):
                return {
                    'success': False,
                    'error': 'Failed to create media container',
                    'details': 'No creation ID received from Instagram API',
                    'api_response': container_response
                }

            creation_id = container_response['id']
            
            # Check media status before publishing
            status = self._check_media_status(creation_id)
            if status.get('status_code') != 'FINISHED':
                return {
                    'success': False,
                    'error': 'Media processing failed',
                    'details': f'Status: {status.get("status_code", "Unknown")}',
                    'api_response': status
                }

            # 2. Publish the container
            publish_response = self._publish_container(creation_id)
            print(f"Publish Response: {publish_response}")

            if 'error' in publish_response:
                return {
                    'success': False,
                    'error': 'Publishing failed',
                    'details': publish_response['error'].get('message', 'Unknown error'),
                    'error_type': publish_response['error'].get('type', 'Unknown'),
                    'error_code': publish_response['error'].get('code', 'Unknown')
                }

            if not publish_response.get('id'):
                return {
                    'success': False,
                    'error': 'Failed to publish post',
                    'details': 'No post ID received from Instagram API',
                    'api_response': publish_response
                }

            return {
                'success': True,
                'post_id': publish_response['id'],
                'status': 'Published successfully',
                'permalink': f"https://www.instagram.com/p/{publish_response['id']}"
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _create_media_container(self, media_path: str, caption: str) -> Dict[str, Any]:
        """Create a media container for the image."""
        url = f"{self.base_url}/{self.account_id}/media"
        
        # Validate file type
        valid_extensions = ['.jpg', '.jpeg', '.png']
        file_ext = os.path.splitext(media_path)[1].lower()
        if file_ext not in valid_extensions:
            return {
                'error': {
                    'message': f'Invalid file type. Must be one of: {", ".join(valid_extensions)}',
                    'type': 'FileTypeError',
                    'code': 400
                }
            }

        try:
            # Instagram requires a URL for the image, so we need to upload it first
            params = {
                'access_token': self.access_token,
                'caption': caption,
                'image_url': 'https://graph.facebook.com',  # This is a placeholder
            }
            
            # First, create the container
            with open(media_path, 'rb') as image_file:
                files = {
                    'image': image_file
                }
                response = requests.post(url, data=params, files=files)
                
            print(f"API Response for media container creation: {response.text}")
            return response.json()
            
        except Exception as e:
            return {
                'error': {
                    'message': f'Failed to create media container: {str(e)}',
                    'type': 'APIError',
                    'code': 500
                }
            }

    def _publish_container(self, creation_id: str) -> Dict[str, Any]:
        """Publish the media container."""
        url = f"{self.base_url}/{self.account_id}/media_publish"
        
        params = {
            'access_token': self.access_token,
            'creation_id': creation_id
        }
        
        response = requests.post(url, params=params)
        return response.json()

    def _check_media_status(self, creation_id: str) -> Dict[str, Any]:
        """Check the status of a media container."""
        url = f"{self.base_url}/{creation_id}"
        
        params = {
            'access_token': self.access_token,
            'fields': 'status_code,status'
        }
        
        response = requests.get(url, params=params)
        return response.json()
