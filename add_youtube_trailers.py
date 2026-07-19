import json
import urllib.request
import urllib.parse
import re
import time
import os

def main():
    if not os.path.exists('movies_data.json'):
        print("Error: movies_data.json not found!")
        return

    with open('movies_data.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)

    updated = False
    for i, movie in enumerate(movies):
        if 'youtube_id' not in movie or not movie['youtube_id']:
            query = f"{movie['title']} {movie['year']} trailer"
            print(f"Searching trailer for: {query}")
            url_query = urllib.parse.quote(query)
            try:
                html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={url_query}').read().decode('utf-8')
                match = re.search(r'"videoId":"([^"]+)"', html)
                if match:
                    movie['youtube_id'] = match.group(1)
                    print(f" Found ID: {movie['youtube_id']}")
                    updated = True
                else:
                    print(" No ID found")
            except Exception as e:
                print(f" Error searching {query}: {e}")
            
            # small delay to avoid getting blocked
            time.sleep(0.5)

    if updated:
        with open('movies_data.json', 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=2, ensure_ascii=False)
        print("Successfully updated movies_data.json with youtube_ids")
    else:
        print("No new youtube_ids were added.")

if __name__ == '__main__':
    main()
