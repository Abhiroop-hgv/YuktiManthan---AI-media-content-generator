import streamlit as st
import asyncio
from async_generator import generate_all_posts, translate_text, platform_styles, LANGUAGES
from social_media_manager import SocialMediaManager
import os
import random
from dotenv import load_dotenv
from youtube_influencers import find_influencers

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Set page configuration
st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="📱",
    layout="wide"
)

# Platform logos in base64
PLATFORM_LOGOS = {
    'linkedin': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZGF0YS1zdXBwb3J0ZWQtZHBpPSIxIj48cGF0aCBmaWxsPSIjMDA3N0I1IiBkPSJNMjAuNSAyaC0xN0ExLjUgMS41IDAgMDAyIDMuNXYxN0ExLjUgMS41IDAgMDAzLjUgMjJoMTdhMS41IDEuNSAwIDAwMS41LTEuNXYtMTdBMS41IDEuNSAwIDAwMjAuNSAyek03LjUgMTguNWgtM3YtOWgzdjl6TTYgOGExLjc1IDEuNzUgMCAxMTEuNzUtMS43NUExLjc1IDEuNzUgMCAwMTYgOHptMTIgMTAuNWgtM3YtNC41N2MwLTEuNDItLjUyLTIuNDMtMS44My0yLjQzYTEuOTUgMS45NSAwIDAwLTEuODIgMS4zMSAxLjc4IDEuNzggMCAwMC0uMDguNjR2NS4wNWgtM3MuMDQtOC4yIDAtOWgzdjEuMjdhMy42IDMuNiAwIDAxMy4yNi0xLjhjMi4zOCAwIDQuMTcgMS41NSA0LjE3IDQuODl2NC42M3oiPjwvcGF0aD48L3N2Zz4=',
    'twitter': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzFEQTFGMiIgZD0iTTIzLjk1MyA0LjU3YTEwIDEwIDAgMDEtMi44MjUuNzc1IDQuOTU4IDQuOTU4IDAgMDAyLjE2My0yLjcyM2MtLjk1MS41NTUtMi4wMDUuOTU5LTMuMTI3IDEuMTg0YTQuOTIgNC45MiAwIDAwLTguMzg0IDQuNDgyQzcuNjkgOC4wOTUgNC4wNjcgNi4xMyAxLjY0IDMuMTYyYTQuODIyIDQuODIyIDAgMDAtLjY2NiAyLjQ3NWMwIDEuNzEuODcgMy4yMTMgMi4xODggNC4wOTZhNC45MDQgNC45MDQgMCAwMS0yLjIyOC0uNjE2di4wNmE0LjkyMyA0LjkyMyAwIDAwMy45NDYgNC44MjcgNC45OTYgNC45OTYgMCAwMS0yLjIxMi4wODUgNC45MzYgNC45MzYgMCAwMDQuNjA0IDMuNDE3IDkuODY3IDkuODY3IDAgMDEtNi4xMDIgMi4xMDVjLS4zOSAwLS43NzktLjAyMy0xLjE3LS4wNjdhMTMuOTk1IDEzLjk5NSAwIDAwNy41NTcgMi4yMDljOS4wNTMgMCAxMy45OTgtNy40OTYgMTMuOTk4LTEzLjk4NSAwLS4yMSAwLS40Mi0uMDE1LS42M0E5LjkzNSA5LjkzNSAwIDAwMjQgNC41OXoiLz48L3N2Zz4=',
    'instagram': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0U0NDA1RiIgZD0iTTEyIDBDOC43NCAwIDguMzMzLjAxNSA3LjA1My4wNzIgNS43NzUuMTMyIDQuOTA1LjMzMyA0LjE0LjYzYy0uNzg5LjMwNi0xLjQ1OS43MTctMi4xMjYgMS4zODRTLjkzNSAzLjM1LjYzIDQuMTRDLjMzMyA0LjkwNS4xMzEgNS43NzUuMDcyIDcuMDUzLjAxMiA4LjMzMyAwIDguNzQgMCAxMnMuMDE1IDMuNjY3LjA3MiA0Ljk0N2MuMDYgMS4yNzcuMjYxIDIuMTQ4LjU1OCAyLjkxMy4zMDYuNzg4LjcxNyAxLjQ1OSAxLjM4NCAyLjEyNi42NjcuNjY2IDEuMzM2IDEuMDc5IDIuMTI2IDEuMzg0Ljc2Ni4yOTYgMS42MzYuNDk5IDIuOTEzLjU1OEMxMC4zMzMgMjMuOTg4IDEwLjc0IDI0IDEyIDI0czEuNjY3LS4wMTUgMi45NDctLjA3MmMxLjI3Ny0uMDYgMi4xNDgtLjI2MiAyLjkxMy0uNTU4Ljc4OC0uMzA2IDEuNDU5LS43MTggMi4xMjYtMS4zODQuNjY2LS42NjcgMS4wNzktMS4zMzUgMS4zODQtMi4xMjYuMjk2LS43NjUuNDk5LTEuNjM2LjU1OC0yLjkxMy4wNi0xLjI4LjA3Mi0xLjY4Ny4wNzItMi45NDdzLS4wMTUtMy42NjctLjA3Mi00Ljk0N2MtLjA2LTEuMjc3LS4yNjItMi4xNDktLjU1OC0yLjkxMy0uMzA2LS43ODktLjcxOC0xLjQ1OS0xLjM4NC0yLjEyNkMyMS4zMTkgMS4zNDcgMjAuNjUxLjkzNSAxOS44Ni42M2MtLjc2NS0uMjk3LTEuNjM2LS40OTktMi45MTMtLjU1OEMxNS42NjcuMDEyIDE1LjI2IDAgMTIgMHptMCAyLjE2YzMuMjAzIDAgMy41ODUuMDE2IDQuODUuMDcxIDEuMTcuMDU1IDEuODA1LjI0OSAyLjIyNy40MTUuNTYyLjIxNy45Ni40NzcgMS4zODIuODk2LjQxOS40MjIuNjc5LjgyLjg5NiAxLjM4Mi4xNjQuNDIyLjM2IDEuMDU3LjQxMyAyLjIyNy4wNTcgMS4yNjYuMDcgMS42NDYuMDcgNC44NXMtLjAxNSAzLjU4NS0uMDc0IDQuODVjLS4wNjEgMS4xNy0uMjU2IDEuODA1LS40MjEgMi4yMjctLjIyNC41NjItLjQ3OS45Ni0uODk5IDEuMzgyLS40MTkuNDE5LS44MjQuNjc5LTEuMzguODk2LS40Mi4xNjQtMS4wNjUuMzYtMi4yMzUuNDEzLTEuMjc0LjA1Ny0xLjY0OS4wNy00Ljg1OS4wNy0zLjIxMSAwLTMuNTg2LS4wMTUtNC44NTktLjA3NC0xLjE3MS0uMDYxLTEuODE2LS4yNTYtMi4yMzYtLjQyMS0uNTY5LS4yMjQtLjk2LS40NzktMS4zNzktLjg5OS0uNDIxLS40MTktLjY5LS44MjQtLjktMS4zOC0uMTY1LS40Mi0uMzU5LTEuMDY1LS40Mi0yLjIzNS0uMDQ1LTEuMjYtLjA2MS0xLjY0OS0uMDYxLTQuODQ0IDAtMy4xOTYuMDE2LTMuNTg2LjA2MS00Ljg2MS4wNjEtMS4xNy4yNTUtMS44MTQuNDItMi4yMzQuMjEtLjU3LjQ3OS0uOTYuOS0xLjM4MS40MTktLjQxOS44MS0uNjg5IDEuMzc5LS44OTguNDItLjE2NiAxLjA1MS0uMzYxIDIuMjIxLS40MjEgMS4yNzUtLjA0NSAxLjY1LS4wNiA0Ljg1OS0uMDZsLjA0NS4wM3ptMCAzLjY3OGE2LjE2MiA2LjE2MiAwIDEwMCAxMi4zMjQgNi4xNjIgNi4xNjIgMCAwMDAtMTIuMzI0ek0xMiAxNmE0IDQgMCAxMTAtOCA0IDQgMCAwMTAgOHpNMTguNDA2IDUuNjJhMS40NCAxLjQ0IDAgMTAwLTIuODggMS40NCAxLjQ0IDAgMDAwIDIuODh6Ii8+PC9zdmc+',
    'youtube': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0ZGMDAwMCIgZD0iTTIzLjQ5NSA2LjIwNWEzLjAwNyAzLjAwNyAwIDAwLTIuMDg4LTIuMDg4Yy0xLjg3LS41MDEtOS4zOTYtLjUwMS05LjM5Ni0uNTAxcy03LjUwNy0uMDEtOS4zOTYuNTAxQTMuMDA3IDMuMDA3IDAgMDAuNTI3IDYuMjA1YTMxLjI0NyAzMS4yNDcgMCAwMC0uNTIyIDUuODA1IDMxLjI0NyAzMS4yNDcgMCAwMC41MjIgNS43ODMgMy4wMDcgMy4wMDcgMCAwMDIuMDg4IDIuMDg4YzEuODY4LjUwMiA5LjM5Ni41MDIgOS4zOTYuNTAyczc1MDctLjAwOSA5LjM5Ni0uNTAyYTMuMDA3IDMuMDA3IDAgMDAyLjA4OC0yLjA4OCAzMS4yNDcgMzEuMjQ3IDAgMDAuNS01Ljc4MyAzMS4yNDcgMzEuMjQ3IDAgMDAtLjUtNS44MDV6TTkuNjA5IDE1LjYwMVY4LjQwOGw2LjI2NCAzLjYwMnoiLz48L3N2Zz4=',
    'email': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzRBNTU2OCIgZD0iTTIwIDRINGMtMS4xIDAtMS45OS45LTEuOTkgMkwyIDE4YzAgMS4xLjkgMiAyIDJoMTZjMS4xIDAgMi0uOSAyLTJWNmMwLTEuMS0uOS0yLTItMnptMCAxNEg0VjhoMTZ2MTB6TTQgNmgxNnYySDRWNnoiLz48L3N2Zz4='
}

# Custom CSS for beautiful UI
st.markdown("""
    <style>
        /* Main App Styling */
        .stApp {
            background: linear-gradient(120deg, #E6F0FF 0%, #F5F8FF 100%);
        }
        
        /* Platform Icon Styling */
        .platform-icon {
            width: 24px;
            height: 24px;
            margin-right: 8px;
            vertical-align: middle;
            display: inline-block;
        }
        
        /* Image Preview Styling */
        .image-preview {
            max-width: 300px !important;
            max-height: 300px !important;
            object-fit: cover !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            margin: 16px 0 !important;
        }
        
        .image-preview-container {
            background: #F8FAFC !important;
            padding: 16px !important;
            border-radius: 12px !important;
            border: 2px dashed #E2E8F0 !important;
            margin: 16px 0 !important;
            text-align: center !important;
        }
        
        .platform-header {
            display: flex !important;
            align-items: center !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            padding-bottom: 12px !important;
            border-bottom: 2px solid #E2E8F0 !important;
            margin-bottom: 16px !important;
        }
        
        /* Custom Container Styling */
        .custom-container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(149, 157, 165, 0.15);
            margin-bottom: 2rem;
        }
        
        /* Input Elements Styling */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div {
            background-color: white !important;
            color: #1A1A1A !important;
            border: 2px solid #E1E4E8 !important;
            border-radius: 12px !important;
            padding: 12px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: #6B46C1 !important;
            box-shadow: 0 0 0 3px rgba(107, 70, 193, 0.2) !important;
        }
        
        /* Button Styling */
        .stButton>button {
            background: linear-gradient(135deg, #6B46C1 0%, #553C9A 100%) !important;
            color: white !important;
            padding: 12px 24px !important;
            border-radius: 30px !important;
            border: none !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 16px rgba(107, 70, 193, 0.2) !important;
        }
        
        /* Selectbox Styling */
.stSelectbox div[data-baseweb="select"] {
    background: white !important;
    border: 2px solid #E1E4E8 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #1A1A1A !important;   /* Make selected text dark */
    font-size: 16px !important;
}

        /* Ensure selectbox selected value and placeholder are visible on white backgrounds */
        .stSelectbox, .stSelectbox * {
            color: #1A1A1A !important;
        }

        .stSelectbox input::placeholder {
            color: #6B7280 !important;
            opacity: 1 !important;
        }
        
        div[role="listbox"] {
            background: white !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            border: none !important;
        }
        
        div[role="listbox"] ul {
            background: white !important;
            padding: 8px !important;
        }
        
        div[role="listbox"] li {
            color: #1A1A1A !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        
        div[role="listbox"] li:hover {
            background: #F4F0FF !important;
            color: #6B46C1 !important;
        }
        
        /* Typography */
        h1 {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            text-align: center !important;
            margin: 2rem 0 !important;
            color: #2D3748 !important;
            letter-spacing: -0.5px !important;
        }
        
        h3 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #2D3748 !important;
            margin: 1.5rem 0 1rem 0 !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 2px solid #E2E8F0 !important;
        }
        
        /* Platform Section Styling */
        .platform-section {
            background: white !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin: 16px 0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        }
        
        /* Labels and Text */
        label, .stMarkdown p {
            color: #4A5568 !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
        }
        
        /* File Uploader Styling */
        .stFileUploader {
            padding: 20px !important;
            border: 2px dashed #E1E4E8 !important;
            border-radius: 16px !important;
            background: #F8FAFC !important;
        }
        
        /* Platform Content Boxes */
        .content-box {
            background: white !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border: 2px solid #E1E4E8 !important;
            margin-bottom: 20px !important;
        }
        
        .content-box:hover {
            border-color: #6B46C1 !important;
            box-shadow: 0 4px 12px rgba(107, 70, 193, 0.1) !important;
        }
        
        /* Influencer Card Styling */
        .influencer-card {
            background: white !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin: 12px 0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.3s ease !important;
            border: 1px solid #E1E4E8 !important;
        }
        
        .influencer-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
        }
        
        .influencer-stats {
            color: #6B46C1 !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize social media manager
if 'social_manager' not in st.session_state:
    st.session_state.social_manager = SocialMediaManager()
    asyncio.run(st.session_state.social_manager.connect_platforms())

# Add title and description with enhanced styling
st.markdown("""
    <div style='text-align: center; padding: 40px 0 20px 0;'>
        <h1 style='color: #2D3748; font-size: 3rem; font-weight: 800; margin-bottom: 1rem;'>
            ✨ Social Media Content Generator
        </h1>
        <div style='max-width: 800px; margin: 0 auto;'>
            <div style='background: white; padding: 24px; border-radius: 16px; box-shadow: 0 8px 24px rgba(149, 157, 165, 0.15);'>
                <p style='font-size: 1.2rem; color: #4A5568; line-height: 1.8; margin: 0;'>
                    Transform your ideas into engaging social media content across multiple platforms. Our AI-powered tool 
                    crafts perfectly tailored messages for each platform, helping you maintain a consistent and 
                    professional presence across all your social channels.
                </p>
                <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
                    <div style='text-align: center; color: #6B46C1;'>
                        <div style='font-size: 1.5rem; margin-bottom: 8px;'>🎯</div>
                        <div style='font-weight: 600;'>Platform-Optimized</div>
                    </div>
                    <div style='text-align: center; color: #6B46C1;'>
                        <div style='font-size: 1.5rem; margin-bottom: 8px;'>🤖</div>
                        <div style='font-weight: 600;'>AI-Powered</div>
                    </div>
                    <div style='text-align: center; color: #6B46C1;'>
                        <div style='font-size: 1.5rem; margin-bottom: 8px;'>⚡</div>
                        <div style='font-weight: 600;'>Instant Results</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create a container for input controls
st.markdown("""
    <div class="custom-container">
        <h3 style='color: #2D3748; margin-bottom: 1.5rem; border: none !important;'>
            Create Your Campaign
        </h3>
    </div>
""", unsafe_allow_html=True)

 # --- Left dashboard (sidebar) with button navigation ---
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0;'>
        <h2 style='color: #2D3748; margin: 0;'>📊 Dashboard</h2>
        <p style='color: #6B46C1; margin-top: 4px;'>Navigate pages</p>
    </div>
    """, unsafe_allow_html=True)

    # Campaign button
    if st.button("Campaign", key="nav_campaign"):
        st.session_state['page'] = 'home'

    # Influencer Links: always show the button; show an error if no campaign content exists
    if st.button("Influencer Links", key="nav_influencers"):
        if st.session_state.get('last_prompt'):
            st.session_state['page'] = 'influencers'
        else:
            st.error("Please generate content on the Campaign page first to search for relevant influencers.")

    # Post Insights button
    if st.button("Post Insights", key="nav_insights"):
        st.session_state['page'] = 'insights'

# Default page
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Page: Influencers
if st.session_state['page'] == 'influencers':
    st.markdown("""
        <div style='background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);'>
            <h2 style='margin: 0; color: #2D3748;'>🔎 Influencer Links</h2>
            <p style='color: #4A5568;'>Search and view influencer channels (YouTube). You can provide a query below.</p>
        </div>
    """, unsafe_allow_html=True)

    # Use the last generated campaign prompt as the query for influencers
    query = st.session_state.get('last_prompt') or ''
    if not query:
        st.warning("No campaign prompt found. Generate content in the Campaign page first.")
    else:
        # Only run search if we don't have results for this prompt yet
        if 'influencers' not in st.session_state or st.session_state.get('influencers_query') != query:
            with st.spinner("Searching YouTube for relevant influencers..."):
                try:
                    influencers = find_influencers(query, api_key=YOUTUBE_API_KEY)
                except Exception as e:
                    st.error(f"Error while searching influencers: {e}")
                    influencers = []
                st.session_state['influencers'] = influencers
                st.session_state['influencers_query'] = query

    # Render results if present
    if 'influencers' in st.session_state and st.session_state['influencers']:
        for inf in st.session_state['influencers']:
            name = inf.get("channel", "Unknown")
            subs = inf.get("subs", 0)
            mentions = inf.get("mentions", 0)
            link = inf.get("link", "#")
            if subs >= 1000000:
                sub_count = f"{subs/1000000:.1f}M"
            elif subs >= 1000:
                sub_count = f"{subs/1000:.1f}K"
            else:
                sub_count = str(subs)
            st.markdown(f"""
                <div class='influencer-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <a href='{link}' target='_blank' style='text-decoration: none;'>
                                <h3 style='color: #6B46C1 !important; margin: 0 !important; border: none !important; font-size: 1.2rem !important;'>{name}</h3>
                            </a>
                            <div style='margin-top: 8px; color: #4A5568;'>
                                <span class='influencer-stats'>📊 {sub_count}</span> subscribers • 
                                <span class='influencer-stats'>🎥 {mentions}</span> related videos
                            </div>
                        </div>
                        <a href='{link}' target='_blank' style='text-decoration: none;'>
                            <div style='background: #F4F0FF; padding: 8px 16px; border-radius: 20px; color: #6B46C1; font-weight: 600;'>
                                View Channel
                            </div>
                        </a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No influencer results yet. Use the search above or generate content and try again.")

    st.stop()

# Page: Insights
if st.session_state['page'] == 'insights':
    st.markdown("""
        <div style='background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);'>
            <h2 style='margin: 0; color: #2D3748;'>📈 Post Insights</h2>
            <p style='color: #4A5568;'>Generate or view mock insights for the latest campaign.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Generate Insights"):
        if 'last_prompt' not in st.session_state or not st.session_state.get('last_prompt'):
            st.warning("Generate content first so insights can be based on the latest campaign.")
        else:
            with st.spinner("Generating post insights..."):
                # Generate platform-specific insights with more realistic numbers
                insights = {
                    'linkedin': {
                        'impressions': random.randint(500, 2000),
                        'reactions': random.randint(20, 100),
                        'comments': random.randint(5, 30),
                        'shares': random.randint(2, 15)
                    },
                    'twitter': {
                        'impressions': random.randint(300, 1500),
                        'likes': random.randint(10, 50),
                        'retweets': random.randint(2, 20),
                        'replies': random.randint(1, 10)
                    },
                    'instagram': {
                        'reach': random.randint(200, 1000),
                        'likes': random.randint(15, 80),
                        'comments': random.randint(3, 25),
                        'saves': random.randint(5, 30)
                    },
                    'youtube': {
                        'views': random.randint(100, 500),
                        'likes': random.randint(10, 40),
                        'comments': random.randint(2, 15),
                        'watch_time': f"{random.randint(2, 5)}:{random.randint(10, 59):02d}"
                    }
                }
                st.session_state['post_insights'] = insights

    # Display if exists
    if 'post_insights' in st.session_state and st.session_state['post_insights']:
        ins = st.session_state['post_insights']
        
        # LinkedIn Insights
        st.markdown(f"""
            <div class='platform-header' style='margin-top: 20px;'>
                <img src="{PLATFORM_LOGOS['linkedin']}" class="platform-icon" alt="LinkedIn"/>
                LinkedIn Insights
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Impressions", ins['linkedin']['impressions'])
        with col2:
            st.metric("Reactions", ins['linkedin']['reactions'])
        with col3:
            st.metric("Comments", ins['linkedin']['comments'])
        with col4:
            st.metric("Shares", ins['linkedin']['shares'])
            
        # Twitter Insights
        st.markdown(f"""
            <div class='platform-header' style='margin-top: 20px;'>
                <img src="{PLATFORM_LOGOS['twitter']}" class="platform-icon" alt="Twitter"/>
                Twitter Insights
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Impressions", ins['twitter']['impressions'])
        with col2:
            st.metric("Likes", ins['twitter']['likes'])
        with col3:
            st.metric("Retweets", ins['twitter']['retweets'])
        with col4:
            st.metric("Replies", ins['twitter']['replies'])
            
        # Instagram Insights
        st.markdown(f"""
            <div class='platform-header' style='margin-top: 20px;'>
                <img src="{PLATFORM_LOGOS['instagram']}" class="platform-icon" alt="Instagram"/>
                Instagram Insights
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Reach", ins['instagram']['reach'])
        with col2:
            st.metric("Likes", ins['instagram']['likes'])
        with col3:
            st.metric("Comments", ins['instagram']['comments'])
        with col4:
            st.metric("Saves", ins['instagram']['saves'])
            
        # YouTube Insights
        st.markdown(f"""
            <div class='platform-header' style='margin-top: 20px;'>
                <img src="{PLATFORM_LOGOS['youtube']}" class="platform-icon" alt="YouTube"/>
                YouTube Insights
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Views", ins['youtube']['views'])
        with col2:
            st.metric("Likes", ins['youtube']['likes'])
        with col3:
            st.metric("Comments", ins['youtube']['comments'])
        with col4:
            st.metric("Avg Watch Time", ins['youtube']['watch_time'])
    else:
        st.info("No insights yet. Click 'Generate Mock Insights' to create sample data.")

    st.stop()


# Create input controls vertically
# Create input text area with enhanced styling
user_prompt = st.text_area(
    "✍️ Enter your campaign idea:",
    height=100,
    placeholder="Describe your campaign or content idea here...",
    help="Be specific about your campaign goals and target audience for better results"
)

# Add language selection with enhanced styling
target_language = st.selectbox(
    "🌍 Select Language",
    options=list(LANGUAGES.keys()),
    format_func=lambda x: x,
    help="Choose the language for your content"
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
    # Clear previous influencer results so the new prompt triggers a fresh search
    st.session_state.pop('influencers', None)
    st.session_state.pop('influencers_query', None)

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
    # Create a container for the preview
    preview_container = st.container()
    with preview_container:
        st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
        st.image(media_file, width=300)  # Set fixed width for preview
        st.markdown('</div>', unsafe_allow_html=True)

# (In-page influencer search removed — use the dashboard 'Get Influencer Links' in the sidebar)

# Render influencer results if available
if 'influencers' in st.session_state and st.session_state['influencers']:
    st.markdown("""
        <div style='background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
            <h2 style='color: #2D3748; font-size: 1.8rem; margin-bottom: 1.5rem;'>
                🔎 Relevant YouTube Influencers
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    for inf in st.session_state['influencers']:
        name = inf.get("channel", "Unknown")
        subs = inf.get("subs", 0)
        mentions = inf.get("mentions", 0)
        link = inf.get("link", "#")
        
        # Format subscriber count
        if subs >= 1000000:
            sub_count = f"{subs/1000000:.1f}M"
        elif subs >= 1000:
            sub_count = f"{subs/1000:.1f}K"
        else:
            sub_count = str(subs)
            
        st.markdown(f"""
            <div class='influencer-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <a href='{link}' target='_blank' style='text-decoration: none;'>
                            <h3 style='color: #6B46C1 !important; margin: 0 !important; border: none !important; font-size: 1.2rem !important;'>
                                {name}
                            </h3>
                        </a>
                        <div style='margin-top: 8px; color: #4A5568;'>
                            <span class='influencer-stats'>📊 {sub_count}</span> subscribers • 
                            <span class='influencer-stats'>🎥 {mentions}</span> related videos
                        </div>
                    </div>
                    <a href='{link}' target='_blank' style='text-decoration: none;'>
                        <div style='background: #F4F0FF; padding: 8px 16px; border-radius: 20px; color: #6B46C1; font-weight: 600;'>
                            View Channel
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

# Render post insights if generated
if 'post_insights' in st.session_state and st.session_state['post_insights']:
    ins = st.session_state['post_insights']
    st.markdown("""
        <div style='background: white; padding: 16px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-top: 12px;'>
            <h3 style='color: #2D3748;'>📈 Post Insights (mock)</h3>
            <p style='color: #4A5568;'>Summary of how your latest post is performing (generated).</p>
        </div>
    """, unsafe_allow_html=True)

    # Display total impressions across platforms
    total_impressions = (
        ins['linkedin']['impressions'] +
        ins['twitter']['impressions'] +
        ins['instagram']['reach'] +
        ins['youtube']['views']
    )
    
    # Display total engagement across platforms
    total_engagement = (
        ins['linkedin']['reactions'] + ins['linkedin']['comments'] + ins['linkedin']['shares'] +
        ins['twitter']['likes'] + ins['twitter']['retweets'] + ins['twitter']['replies'] +
        ins['instagram']['likes'] + ins['instagram']['comments'] + ins['instagram']['saves'] +
        ins['youtube']['likes'] + ins['youtube']['comments']
    )
    
    # Calculate overall engagement rate
    engagement_rate = round((total_engagement / total_impressions) * 100, 2)
    
    # Display overall metrics
    st.metric("Total Reach/Views", total_impressions)
    c1, c2 = st.columns(2)
    c1.metric("Total Engagements", total_engagement)
    c2.metric("Overall Engagement Rate", f"{engagement_rate}%")

# Display the generated platform content and publishing UI
if 'all_posts' in locals():
    st.markdown("""
        <div style='margin-top: 32px;'>
            <h2 style='color: #2D3748; margin-bottom: 24px;'>Generated Content</h2>
        </div>
    """, unsafe_allow_html=True)

    # Define platforms in a vertical layout
    platforms = [
        ("LinkedIn 👔", "linkedin", True),
        ("Twitter �", "twitter", True),
        ("Instagram �", "instagram", True),
        ("YouTube 🎥", "youtube", True),
        ("Email ✉️", "email", False)  # Email doesn't have a post button
    ]

    # LinkedIn
    with st.container():
        st.markdown("""
            <div class='social-content-box'>
                <div class='platform-header'>
                <img src=""" + PLATFORM_LOGOS['linkedin'] + """ class="platform-icon" alt="LinkedIn"/>
                LinkedIn
            </div>
        """, unsafe_allow_html=True)
        linkedin_text = st.text_area("", all_posts['linkedin'], key="linkedin", height=150)
        if st.button("Post to LinkedIn", key="linkedin_post"):
            with st.spinner("Publishing to LinkedIn..."):
                media_path = st.session_state.social_manager.save_media_file(media_file) if media_file else None
                success = asyncio.run(st.session_state.social_manager.publish_to_linkedin(linkedin_text, media_path))
                if success:
                    st.success("Published to LinkedIn!")
                else:
                    st.error("Failed to publish to LinkedIn")
        st.markdown("</div>", unsafe_allow_html=True)

    # Twitter
    with st.container():
        st.markdown("""
            <div class='social-content-box'>
                <div class='platform-header'>
                <img src=""" + PLATFORM_LOGOS['twitter'] + """ class="platform-icon" alt="Twitter"/>
                Twitter
            </div>
        """, unsafe_allow_html=True)
        twitter_text = st.text_area("", all_posts['twitter'], key="twitter", height=150)
        if st.button("Post to Twitter", key="twitter_post"):
            with st.spinner("Publishing to Twitter..."):
                media_path = st.session_state.social_manager.save_media_file(media_file) if media_file else None
                success = asyncio.run(st.session_state.social_manager.publish_to_twitter(twitter_text, media_path))
                if success:
                    st.success("Published to Twitter!")
                else:
                    st.error("Failed to publish to Twitter")
        st.markdown("</div>", unsafe_allow_html=True)

    # Instagram
    with st.container():
        st.markdown("""
            <div class='social-content-box'>
                <div class='platform-header'>
                <img src=""" + PLATFORM_LOGOS['instagram'] + """ class="platform-icon" alt="Instagram"/>
                Instagram
                </div>
            """, unsafe_allow_html=True)
        instagram_text = st.text_area("", all_posts['instagram'], key="instagram", height=150)
        if st.button("Post to Instagram", key="instagram_post"):
            if not media_file:
                st.error("Instagram requires an image to post")
            else:
                with st.spinner("Publishing to Instagram..."):
                    media_path = st.session_state.social_manager.save_media_file(media_file)
                    success = asyncio.run(st.session_state.social_manager.publish_to_instagram(instagram_text, media_path))
                    if success:
                        st.success("Published to Instagram!")
                    else:
                        st.error("Failed to publish to Instagram")
        st.markdown("</div>", unsafe_allow_html=True)

        # YouTube
        with st.container():
            st.markdown("""
                <div class='social-content-box'>
                    <div class='platform-header'>
                    <img src=""" + PLATFORM_LOGOS['youtube'] + """ class="platform-icon" alt="YouTube"/>
                    YouTube
                </div>
            """, unsafe_allow_html=True)
            youtube_text = st.text_area("", all_posts['youtube'], key="youtube")
            if st.button("Post to YouTube", key="youtube_post"):
                if not media_file or not media_file.name.endswith('.mp4'):
                    st.error("YouTube requires a video file")
                else:
                    with st.spinner("Publishing to YouTube..."):
                        media_path = st.session_state.social_manager.save_media_file(media_file)
                        success = asyncio.run(st.session_state.social_manager.publish_to_youtube(youtube_text, media_path))
                        if success:
                            st.success("Published to YouTube!")
                        else:
                            st.error("Failed to publish to YouTube")
            st.markdown("</div>", unsafe_allow_html=True)

    # Email in a separate row
    st.markdown("""
        <div class='social-content-box' style='margin-top: 24px;'>
            <div class='platform-header'>
                <img src=""" + PLATFORM_LOGOS['email'] + """ class="platform-icon" alt="Email"/>
                Email
            </div>
    """, unsafe_allow_html=True)
    email_text = st.text_area("", all_posts['email'], key="email")
    st.markdown("</div>", unsafe_allow_html=True)

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

# Add space at the bottom for better layout
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
