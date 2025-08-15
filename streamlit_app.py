import streamlit as st
import asyncio
from async_generator import generate_all_posts, translate_text, platform_styles, LANGUAGES
from social_media_manager import SocialMediaManager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="📱",
    layout="wide"
)

# Initialize social media manager
if 'social_manager' not in st.session_state:
    st.session_state.social_manager = SocialMediaManager()
    asyncio.run(st.session_state.social_manager.connect_platforms())

# Add title and description
st.title("✨ Social Media Content Generator")
st.markdown("""
Enter your campaign idea or topic, and we'll generate tailored content for different social media platforms.
""")

# Create two columns for input controls
input_col1, input_col2 = st.columns([3, 1])

with input_col1:
    # Create input text area
    user_prompt = st.text_area("Enter your campaign idea:", height=100)

with input_col2:
    # Add language selection
    target_language = st.selectbox(
        "Select Language",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: x
    )

# Initialize session state
if 'english_content' not in st.session_state:
    st.session_state.english_content = None
if 'translated_content' not in st.session_state:
    st.session_state.translated_content = {}
if 'last_prompt' not in st.session_state:
    st.session_state.last_prompt = None
if 'last_language' not in st.session_state:
    st.session_state.last_language = None

# Function to get translated content
def get_translated_content():
    if st.session_state.english_content is None:
        return None
    
    lang_key = f"{target_language}"
    if lang_key not in st.session_state.translated_content:
        with st.spinner(f'Translating to {target_language}...'):
            lang_code = LANGUAGES[target_language]
            translated = {}
            for platform, content in st.session_state.english_content.items():
                translated[platform] = asyncio.run(translate_text(content, lang_code))
            st.session_state.translated_content[lang_key] = translated
    
    return st.session_state.translated_content[lang_key]

# Handle content generation and display
if st.button("Generate Content", type="primary"):
    if not user_prompt:
        st.warning("Please enter a campaign idea first!")
        st.stop()
    
    # Generate new content in English
    with st.spinner('Generating content...'):
        st.session_state.english_content = asyncio.run(generate_all_posts(user_prompt, 'en'))
        st.session_state.last_prompt = user_prompt
        st.session_state.translated_content = {}  # Clear previous translations
    
    all_posts = get_translated_content() if target_language != "English" else st.session_state.english_content
elif st.session_state.english_content is not None:
    # If content exists and language changed, get translated content
    all_posts = get_translated_content() if target_language != "English" else st.session_state.english_content
else:
    st.info("Click 'Generate Content' to create your social media posts.")
    st.stop()

# Update last language
st.session_state.last_language = target_language

# Add media upload section
media_file = st.file_uploader("Upload Media (Image/Video)", type=['png', 'jpg', 'jpeg', 'gif', 'mp4'])
if media_file:
    st.image(media_file, caption="Uploaded Media Preview", use_column_width=True)

# Display the content
if 'all_posts' in locals():
    col1, col2 = st.columns(2)
    
    # First column
    with col1:
        # LinkedIn
        st.markdown("### LinkedIn 👔")
        linkedin_text = st.text_area("", all_posts['linkedin'], height=200, key="linkedin")
        col1_1, col1_2 = st.columns([3, 1])
        with col1_2:
            if st.button("Post to LinkedIn", key="linkedin_post"):
                with st.spinner("Publishing to LinkedIn..."):
                    media_path = st.session_state.social_manager.save_media_file(media_file) if media_file else None
                    success = asyncio.run(
                        st.session_state.social_manager.publish_to_linkedin(linkedin_text, media_path)
                    )
                    if success:
                        st.success("Published to LinkedIn!")
                    else:
                        st.error("Failed to publish to LinkedIn")
        
        # Twitter
        st.markdown("### Twitter 🐦")
        twitter_text = st.text_area("", all_posts['twitter'], height=150, key="twitter")
        col2_1, col2_2 = st.columns([3, 1])
        with col2_2:
            if st.button("Post to Twitter", key="twitter_post"):
                with st.spinner("Publishing to Twitter..."):
                    media_path = st.session_state.social_manager.save_media_file(media_file) if media_file else None
                    success = asyncio.run(
                        st.session_state.social_manager.publish_to_twitter(twitter_text, media_path)
                    )
                    if success:
                        st.success("Published to Twitter!")
                    else:
                        st.error("Failed to publish to Twitter")
        
        # Email
        st.markdown("### Email ✉️")
        email_text = st.text_area("", all_posts['email'], height=200, key="email")

    # Second column
    with col2:
        # Instagram
        st.markdown("### Instagram 📸")
        instagram_text = st.text_area("", all_posts['instagram'], height=200, key="instagram")
        col3_1, col3_2 = st.columns([3, 1])
        with col3_2:
            if st.button("Post to Instagram", key="instagram_post"):
                if not media_file:
                    st.error("Instagram requires an image to post")
                else:
                    with st.spinner("Publishing to Instagram..."):
                        media_path = st.session_state.social_manager.save_media_file(media_file)
                        success = asyncio.run(
                            st.session_state.social_manager.publish_to_instagram(instagram_text, media_path)
                        )
                        if success:
                            st.success("Published to Instagram!")
                        else:
                            st.error("Failed to publish to Instagram")
        
        # YouTube
        st.markdown("### YouTube 🎥")
        youtube_text = st.text_area("", all_posts['youtube'], height=200, key="youtube")
        col4_1, col4_2 = st.columns([3, 1])
        with col4_2:
            if st.button("Post to YouTube", key="youtube_post"):
                if not media_file or not media_file.name.endswith('.mp4'):
                    st.error("YouTube requires a video file")
                else:
                    with st.spinner("Publishing to YouTube..."):
                        media_path = st.session_state.social_manager.save_media_file(media_file)
                        success = asyncio.run(
                            st.session_state.social_manager.publish_to_youtube(youtube_text, media_path)
                        )
                        if success:
                            st.success("Published to YouTube!")
                        else:
                            st.error("Failed to publish to YouTube")
    
    st.success("Content generated successfully! 🎉")
    
    # Add "Post to All Platforms" button
    if st.button("Post to All Platforms", type="primary"):
        with st.spinner("Publishing to all platforms..."):
            media_path = st.session_state.social_manager.save_media_file(media_file) if media_file else None
            content_dict = {
                'linkedin': linkedin_text,
                'twitter': twitter_text,
                'instagram': instagram_text,
                'youtube': youtube_text
            }
            results = asyncio.run(
                st.session_state.social_manager.publish_to_all(content_dict, media_path)
            )
            
            # Show results
            st.write("Publishing Results:")
            for platform, success in results.items():
                if success:
                    st.success(f"✅ Published to {platform.title()}")
                else:
                    st.error(f"❌ Failed to publish to {platform.title()}")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using AWS Bedrock and Streamlit")
