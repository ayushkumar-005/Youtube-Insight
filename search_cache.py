import sys
import os

def search_cache(video_id, keyword):
    cache_file = os.path.join(".clawhub", "cache", f"{video_id}.txt")
    if not os.path.exists(cache_file):
        return "Error: Transcript cache not found."
        
    with open(cache_file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    idx = text.lower().find(keyword.lower())
    
    if idx == -1:
        return f"No results found for '{keyword}' in the transcript."
        
    start = max(0, idx - 500)
    end = min(len(text), idx + 500)
    return f"...{text[start:end]}..."

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Provide video_id and keyword.")
    else:
        print(search_cache(sys.argv[1], sys.argv[2]))