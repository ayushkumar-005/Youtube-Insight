import sys
import json
import urllib.request
import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

MAX_CHARS = 15000 
CACHE_DIR = ".clawhub/cache"

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1][:11]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1][:11]
    return None

def get_video_title(url):
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req).read().decode('utf-8')
        return json.loads(response).get('title', 'Unknown Title')
    except Exception:
        return "Unknown Title"

def fetch_transcript(url):
    video_id = get_video_id(url)
    
    if not video_id:
        return json.dumps({"status": "error", "message": "Invalid YouTube URL provided."})
        
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{video_id}.txt")
        
    try:
        # 1. Check if we already cached this video
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                full_text = f.read()
        else:
            # 2. If not, fetch it from YouTube and cache it
            ytt_api = YouTubeTranscriptApi()
            fetched_transcript = ytt_api.fetch(video_id)
            full_text = " ".join([snippet.text for snippet in fetched_transcript])
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(full_text)
        
        title = get_video_title(url)
        
        # 3. Truncate for the initial summary to save tokens, but tell the bot where the rest is
        summary_text = full_text
        if len(full_text) > MAX_CHARS:
            summary_text = full_text[:MAX_CHARS] + f"... [SYSTEM NOTE: Transcript truncated to save tokens. To answer follow-up questions about later parts of the video, use the exec tool to run: py search_cache.py \"{video_id}\" \"<search_keyword>\"]"
            
        return json.dumps({
            "status": "success", 
            "title": title,
            "text": summary_text
        })
        
    except (TranscriptsDisabled, NoTranscriptFound):
        return json.dumps({"status": "error", "message": "No transcript available for this video."})
    except VideoUnavailable:
        return json.dumps({"status": "error", "message": "This video is unavailable or does not exist. Please check the link."})
    except Exception as e:
        return json.dumps({"status": "error", "message": "An unexpected error occurred while fetching the transcript. Please try a different video."})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No URL provided."}))
    else:
        print(fetch_transcript(sys.argv[1]))