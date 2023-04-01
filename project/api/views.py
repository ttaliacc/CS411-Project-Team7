from django.shortcuts import render
import requests
from django.http import HttpResponse

# Create your views here.

def main(request):
    return HttpResponse("hello")

TMDB_API_KEY = '3016e6c23565d0fd1b4b0e0953da86d2'

def search(request):
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

    # Render the template with the search results
    return render(request, 'api/results.html', {
        'data': data.json(),
        'type': request.GET.get('type')})

def index(request):
    return render(request, 'api/index.html')

