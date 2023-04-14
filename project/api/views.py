from django.shortcuts import render
import requests
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'api/index.html')

def search(request):
    data = tmdb(request)
    streaming = {}
    for movie in data.json()['results']:
        stream_info = utelly(movie['original_title'])
        if stream_info['results']:
            streaming[movie['id']] = stream_info['results'][0]['locations'][0]
    context = {
        'data': data.json(),
        'streaming': streaming,
        }
    return render(request, 'api/results.html', context)

TMDB_API_KEY = '3016e6c23565d0fd1b4b0e0953da86d2'
UTELLY_API_URL = url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
X_RAPIDAPI_KEY = "45a4c67909msh27c81fcbd07a4fap1a1b86jsn62fd26476f1a"
X_RAPIDAPI_HOST = "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"

def tmdb(request):
    # Get the user's search query from the request
    query = request.GET.get('q')

    # Construct the search request to the API
    if query:
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
        'api_key': TMDB_API_KEY,
        'query': query
        }  

        # Make the request to the API and get the response
        data = requests.get(url, params=params)
    else:
        return HttpResponse("Please enter a search query")
    # type = request.GET.get('type')
    return data

def utelly(keyword):
    headers = {
        "X-RapidAPI-Key": X_RAPIDAPI_KEY,
        "X-RapidAPI-Host": X_RAPIDAPI_HOST
    }
    params = {
        "term": keyword,
        "country": "us"
    }
    data = requests.get(UTELLY_API_URL, headers=headers, params=params)
    streaming = data.json()

    return streaming
    

