import requests
from .nlp_filter import is_educational

API_KEY = 'AIzaSyBmExYFyO1BaBqtgNIqPAWguogPuM20DrQ'

def get_educational_shorts(subject, max_results=10):
    search_query = f'{subject}+shorts'
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={search_query}&type=video&key={API_KEY}'
    
    response = requests.get(search_url)
    if response.status_code == 200:
        video_ids = [item['id']['videoId'] for item in response.json().get('items', [])]
        
        video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id={",".join(video_ids)}&key={API_KEY}'
        details_response = requests.get(video_details_url)

        if details_response.status_code == 200:
            video_details = details_response.json()
            shorts = []
            for item in video_details['items']:
                duration = item['contentDetails']['duration']
                title = item['snippet']['title']
                description = item['snippet']['description']
                video_id = item['id']

                if 'PT1M' not in duration and is_educational(f"{title} {description}"):
                    shorts.append({
                        'title': title,
                        'videoId': video_id,
                        'duration': duration
                    })

                    log_watch_history('user_id', video_id, title)  

            return shorts
    return {'error': 'Failed to fetch shorts'}
