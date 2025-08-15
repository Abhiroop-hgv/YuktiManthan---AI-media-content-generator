import os
import json
from dotenv import load_dotenv
from rich.console import Console
import boto3
from botocore.config import Config

# Load environment variables
load_dotenv()

# Configure AWS
aws_region = os.getenv('AWS_REGION', 'us-west-2')
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

if not all([aws_region, aws_access_key, aws_secret_key]):
    raise ValueError("AWS credentials not found. Please check your .env file.")

config = Config(
    region_name=aws_region,
    retries=dict(
        max_attempts=3
    )
)

# Initialize Bedrock and Bedrock Runtime clients
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    config=config,
    region_name=aws_region
)

bedrock = boto3.client(
    service_name='bedrock',
    config=config,
    region_name=aws_region
)

# Test connection by listing available models
try:
    available_models = bedrock.list_foundation_models()
    print("\nAvailable Bedrock Models:")
    for model in available_models['modelSummaries']:
        print(f"- {model['modelId']}")
except Exception as e:
    print(f"Error listing models: {str(e)}")

console = Console()

# Platform-specific style instructions
platform_styles = {
    "linkedin": "Professional tone, structured in 2-3 paragraphs, with a clear call-to-action for business professionals.",
    "instagram": "Fun, short, emotional, with emojis and 5-8 trending hashtags.",
    "twitter": "Concise, witty, with a strong hook and 1-2 hashtags.",
    "email": "Warm, personal, clear value proposition, ending with a call-to-action link.",
    "youtube": "Engaging intro, story-driven, ending with a call to subscribe."
}

def generate_post(prompt, platform):
    try:
        style_instruction = platform_styles.get(platform.lower(), "Neutral style.")
        prompt_text = f"""
        You are an expert social media copywriter.
        Write a {platform} post about: {prompt}
        Follow this style: {style_instruction}
        """

        # Using Claude model from AWS Bedrock
        body = json.dumps({
            "prompt": f"\n\nHuman: Create a {platform} post about {prompt}. {style_instruction}\n\nAssistant:",
            "max_tokens_to_sample": 2000,
            "temperature": 0.7,
            "top_k": 250,
            "anthropic_version": "bedrock-2023-05-31"
        })

        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-v2",
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response.get('body').read())
        completion = response_body.get('completion', '')
        # Remove any leading/trailing whitespace and "Assistant:" if present
        completion = completion.replace("Assistant:", "").strip()
        return completion
    
    except Exception as e:
        print(f"Error with Bedrock API: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response details: {e.response}")
        return f"Error generating content: {str(e)}"

if __name__ == "__main__":
    topic = input("Enter your campaign idea: ")
    console.rule(f"[bold blue]Generating posts for: {topic}")

    for platform in platform_styles.keys():
        console.print(f"\n[bold green]--- {platform.upper()} ---[/bold green]")
        post = generate_post(topic, platform)
        console.print(post)
