import asyncio
import json
from typing import Dict
import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure AWS
aws_region = os.getenv('AWS_REGION', 'us-west-2')
config = Config(
    region_name=aws_region,
    retries=dict(max_attempts=3)
)

# Language codes mapping
LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Kannada": "kn",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Spanish": "es",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh",
    "Hindi": "hi",
    "Arabic": "ar"
}

# Initialize AWS clients
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    config=config,
    region_name=aws_region
)

translate = boto3.client(
    service_name='translate',
    config=config,
    region_name=aws_region
)

async def translate_text(text: str, target_language: str) -> str:
    """Translate text to target language using AWS Translate."""
    try:
        if target_language == "en" or not target_language:
            return text
            
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: translate.translate_text(
                Text=text,
                SourceLanguageCode='en',
                TargetLanguageCode=target_language
            )
        )
        return response.get('TranslatedText', text)
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text

# Platform-specific style instructions
platform_styles = {
    "linkedin": "Professional tone, structured in 2-3 paragraphs, with a clear call-to-action for business professionals.",
    "instagram": "Fun, short, emotional, with emojis and 5-8 trending hashtags.",
    "twitter": "Concise, witty, with a strong hook and 1-2 hashtags.",
    "email": "Warm, personal, clear value proposition, ending with a call-to-action link.",
    "youtube": "Engaging intro, story-driven, ending with a call to subscribe."
}

async def generate_single_post(prompt: str, platform: str, target_language: str = None) -> str:
    """Generate content for a single platform asynchronously and translate if needed."""
    try:
        style_instruction = platform_styles.get(platform.lower(), "Neutral style.")
        
        body = json.dumps({
            "prompt": f"\n\nHuman: Write only the content for a {platform} post about: {prompt}. {style_instruction} Do not include any introductory text or explanations.\n\nAssistant:",
            "max_tokens_to_sample": 2000,
            "temperature": 0.7,
            "top_k": 250,
            "anthropic_version": "bedrock-2023-05-31"
        })

        # Create event loop to run async operations
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: bedrock_runtime.invoke_model(
                modelId="anthropic.claude-v2",
                body=body,
                contentType="application/json",
                accept="application/json"
            )
        )
        
        response_body = json.loads(response.get('body').read())
        completion = response_body.get('completion', '').replace("Assistant:", "").strip()
        
        # Translate the content if target language is specified
        if target_language and target_language != "en":
            completion = await translate_text(completion, target_language)
            
        return completion
    
    except Exception as e:
        return f"Error generating {platform} content: {str(e)}"

async def generate_all_posts(prompt: str, target_language: str = None) -> Dict[str, str]:
    """Generate content for all platforms concurrently with translation support."""
    tasks = []
    for platform in platform_styles.keys():
        task = generate_single_post(prompt, platform, target_language)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return dict(zip(platform_styles.keys(), results))
