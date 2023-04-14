from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'api/index.html')

def SearchResult(request):
    # Get the search query from the 'q' URL parameter.
    query = request.GET.get('q')
    if query:
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
        'api_key': settings.TMDB_API_KEY,
        'query': query
        }  
        # Call the TMDB API to search for movies with query if it exists.
        response = requests.get(url, params=params)

        # Get the search results from the TMDB API response.
        results = response.json()['results']
        for result in results:
            # Call the Utelly API to get streaming information for each movie.
            response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={result["id"]}&source=tmdb', headers={'x-rapidapi-key': settings.X_RAPIDAPI_KEY, 'x-rapidapi-host': settings.X_RAPIDAPI_HOST})
            
            # Add the streaming information to the search result dictionary.
            result['streaming_info'] = response.json()['collection']
    else:
        # If no search query was provided, return an error message.
        return HttpResponse('Please enter a search query')
    
    context = {'results': results}
    return render(request, 'api/results.html', context)
    # Return the search results with streaming information as a JSON response.

#Currently not supported
def MovieDetail(request, movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}')
    movie = response.json()
    
    response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={movie_id}&source=tmdb', headers={'x-rapidapi-key': settings.X_RAPIDAPI_KEY, 'x-rapidapi-host': settings.X_RAPIDAPI_HOST})
    streaming = response.json()

    return render(request, 'api/movie_detail.html', {'movie': movie,'streaming': streaming})
    

