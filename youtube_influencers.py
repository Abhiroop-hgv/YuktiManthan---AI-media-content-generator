import os
from collections import Counter
from googleapiclient.discovery import build
import spacy
import re
from typing import List, Dict, Optional

# Load spaCy model once at module import; raise helpful error if missing
def _load_spacy():
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        # spaCy or model not available; return None and rely on fallback extractor
        return None

_nlp = _load_spacy()

# Simple fallback stopwords (keeps small, not exhaustive)
_FALLBACK_STOPWORDS = {
    "the","and","for","with","that","this","from","your","you","are","our","have",
    "will","can","not","but","about","product","service","use","using","get","gets",
    "a","an","in","on","of","to","is","it","as","at","by"
}

def _extract_keywords_fallback(text: str, top_n: int = 10) -> List[str]:
    """
    Lightweight fallback extractor:
    - Tokenizes words (letters only), filters short words and stopwords
    - Returns top words by frequency and a few frequent bigrams
    """
    if not text:
        return []
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    filtered = [w for w in words if w not in _FALLBACK_STOPWORDS]
    if not filtered:
        return []
    word_counts = Counter(filtered)
    keywords = [w for w, _ in word_counts.most_common(top_n)]

    # add common bigrams if any
    bigrams = [" ".join([filtered[i], filtered[i+1]]) for i in range(len(filtered)-1)]
    bigram_counts = Counter(bigrams)
    for b, _ in bigram_counts.most_common(5):
        if b not in keywords:
            keywords.append(b)
        if len(keywords) >= top_n:
            break

    return keywords[:top_n]

def extract_keywords(text: str) -> List[str]:
    """
    Extract a set of candidate keywords from text using spaCy noun chunks and entities
    when available. If spaCy/model is not present, a lightweight regex-based fallback
    is used so the app can still find relevant YouTube channels.
    """
    if _nlp and text:
        doc = _nlp(text)
        keywords = set()
        for chunk in doc.noun_chunks:
            if len(chunk.text.strip()) > 2:
                keywords.add(chunk.text.strip())
        for ent in doc.ents:
            if len(ent.text.strip()) > 2:
                keywords.add(ent.text.strip())
        return list(keywords)
    # fallback
    return _extract_keywords_fallback(text)

def search_videos(youtube, query: str, max_results: int = 8):
    """
    Return search results (list of video items) for a query via the youtube client.
    """
    try:
        resp = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results
        ).execute()
        return resp.get("items", [])
    except Exception:
        return []

def get_channel_stats(youtube, channel_ids: List[str]) -> Dict[str, Dict]:
    """
    Fetch channel statistics (title, subscriber count, link) for a list of channel ids.
    """
    try:
        resp = youtube.channels().list(
            part="statistics,snippet",
            id=",".join(channel_ids)
        ).execute()
    except Exception:
        return {}
    stats = {}
    for item in resp.get("items", []):
        stats[item["id"]] = {
            "title": item["snippet"]["title"],
            "subs": int(item["statistics"].get("subscriberCount", 0)),
            "link": f"https://www.youtube.com/channel/{item['id']}"
        }
    return stats

def find_influencers(
    description: str,
    api_key: Optional[str] = None,
    max_results_per_keyword: int = 6,
    top_n: int = 10
) -> List[Dict]:
    """
    Main entrypoint: given a product/ campaign description, return a ranked list of influencer
    channel dicts with keys: channel, subs, link, mentions.

    - api_key: YouTube Data API key. If None, will attempt to read env var YOUTUBE_API_KEY.
    - Returns [] on error or when no influencers found.
    """
    if not api_key:
        api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        # Caller should handle missing API key
        raise RuntimeError("YOUTUBE_API_KEY not provided")

    youtube = build("youtube", "v3", developerKey=api_key)
    keywords = extract_keywords(description) if description else []
    if not keywords:
        return []

    channel_frequency = Counter()
    for keyword in keywords:
        videos = search_videos(youtube, keyword, max_results=max_results_per_keyword)
        for vid in videos:
            channel_id = vid.get("snippet", {}).get("channelId")
            if channel_id:
                channel_frequency[channel_id] += 1

    if not channel_frequency:
        return []

    top_channels = [cid for cid, _ in channel_frequency.most_common(top_n)]
    stats = get_channel_stats(youtube, top_channels)

    ranked = sorted(
        stats.items(),
        key=lambda x: (channel_frequency.get(x[0], 0), x[1]["subs"]),
        reverse=True
    )

    influencers = []
    for channel_id, data in ranked:
        influencers.append({
            "channel": data["title"],
            "subs": data["subs"],
            "link": data["link"],
            "mentions": channel_frequency.get(channel_id, 0)
        })
    return influencers
