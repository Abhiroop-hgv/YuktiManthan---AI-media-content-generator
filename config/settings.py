# Social Media Configuration
SOCIAL_MEDIA_CONFIG = {
    'linkedin': {
        'client_id': 'YOUR_LINKEDIN_CLIENT_ID',
        'client_secret': 'YOUR_LINKEDIN_CLIENT_SECRET',
        'access_token': 'YOUR_LINKEDIN_ACCESS_TOKEN'
    },
    'twitter': {
        'api_key': 'YOUR_TWITTER_API_KEY',
        'api_secret': 'YOUR_TWITTER_API_SECRET',
        'access_token': 'YOUR_TWITTER_ACCESS_TOKEN',
        'access_token_secret': 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'
    },
    'instagram': {
        'app_id': 'YOUR_INSTAGRAM_APP_ID',
        'app_secret': 'YOUR_INSTAGRAM_APP_SECRET',
        'access_token': 'YOUR_INSTAGRAM_ACCESS_TOKEN'
    },
    'youtube': {
        'api_key': 'YOUR_YOUTUBE_API_KEY',
        'client_id': 'YOUR_YOUTUBE_CLIENT_ID',
        'client_secret': 'YOUR_YOUTUBE_CLIENT_SECRET'
    }
}

# File upload configuration
ALLOWED_IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# API endpoints
API_ENDPOINTS = {
    'linkedin': 'https://api.linkedin.com/v2/ugcPosts',
    'twitter': 'https://api.twitter.com/2/tweets',
    'instagram': 'https://graph.instagram.com/me/media',
    'youtube': 'https://www.googleapis.com/youtube/v3/videos'
}
