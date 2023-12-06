import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect

def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_query = request.POST.get('search', None)
        if search_query:
            search_params = {
                'part' : 'snippet',
                'q' : search_query,
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'maxResults' : 90,
                'type' : 'video',
                'videoCategoryId': '27',  # limit to educational videos only
            }

            r = requests.get(search_url, params=search_params)

            results = r.json().get('items', [])

            video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])

            if request.POST.get('submit') == 'lucky':
                return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

            video_params = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet,contentDetails',
                'id' : ','.join(video_ids),
                'maxResults' : 91
            }

            r = requests.get(video_url, params=video_params)

            results = r.json().get('items', [])

            for result in results:
                video_data = {
                    'title' : result['snippet']['title'],
                    'id' : result['id'],
                    'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                    'category': result['snippet']['categoryId']
                }

                videos.append(video_data)
        else:
            # display educational courses videos by default
            search_params = {
                'part': 'snippet',
                'q': 'educational courses',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'maxResults': 90,
                'type': 'video',
                'videoCategoryId': '27',  # limit to educational videos only
            }

            r = requests.get(search_url, params=search_params)

            results = r.json().get('items', [])

            video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])

            video_params = {
                'key': settings.YOUTUBE_DATA_API_KEY,
                'part': 'snippet,contentDetails',
                'id': ','.join(video_ids),
                'maxResults': 90
            }

            r = requests.get(video_url, params=video_params)

            results = r.json().get('items', [])

            for result in results:
                video_data = {
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                    'category': result['snippet']['categoryId']
                }

                videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'search/index.html', context)

