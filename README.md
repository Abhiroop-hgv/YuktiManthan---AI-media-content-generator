# YuktiManthan - AI Media Content Generator

A powerful social media content generator that uses AWS Bedrock for content generation and supports posting to multiple social media platforms.

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

# Instagram API Credentials
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id
```

5. Setting up Instagram Credentials:
   - Create a Meta Developer Account: https://developers.facebook.com/
   - Create a new app or use an existing one
   - Enable Instagram Graph API
   - Get your Instagram Business Account ID using Graph API Explorer
   - Generate a long-lived access token

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. The web interface will open in your default browser

## Features

- Content generation using AWS Bedrock
- Image and text post creation
- Direct posting to Instagram
- Media file handling and processing
- Asynchronous operations for better performance

## Important Notes

1. Instagram Requirements:
   - Business/Professional Instagram account
   - Connected Facebook Page
   - Valid Meta Developer App with proper permissions
   - Long-lived access token

2. AWS Requirements:
   - AWS account with Bedrock access
   - Valid credentials with proper permissions

## Troubleshooting

If you encounter issues:

1. Check your `.env` file has all required credentials
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
