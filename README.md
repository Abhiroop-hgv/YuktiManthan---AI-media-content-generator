# YuktiManthan - AI Media Content Generator

A powerful content generator that uses AWS Bedrock for content generation and helps you find relevant YouTube influencers.

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd YuktiManthan
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add the following configurations:
```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region

# YouTube API Key
YOUTUBE_API_KEY=your_youtube_api_key
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. The web interface will open in your default browser

## Features

- Content generation using AWS Bedrock
- Content translation to multiple languages
- Find relevant YouTube influencers for your campaign/topic

## Important Notes

1. AWS Requirements:
   - AWS account with Bedrock access
   - Valid credentials with proper permissions

2. YouTube Requirements:
   - Valid YouTube Data API key

## Troubleshooting

If you encounter issues:

1. Check your `.env` file has all required credentials
2. Ensure your AWS and YouTube API keys are correct

## Security Notes

- Never commit your `.env` file
- Keep your access tokens secure
- Regularly rotate your credentials
- Monitor your API usage

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Submit an issue in the repository
3. Contact the maintainers
2. Ensure your Instagram account is properly set up as a Business account
3. Verify your access token has required permissions:
   - instagram_basic
   - instagram_content_publish

## Security Notes

- Never commit your `.env` file
- Keep your access tokens secure
- Regularly rotate your credentials
- Monitor your API usage

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Submit an issue in the repository
3. Contact the maintainers
# YuktiManthan---AI-media-content-generator
Social Media Content Generator with Instagram
>>>>>>> 89f5763c0b9862a19c750a3e9c08e1d2bf8192db
