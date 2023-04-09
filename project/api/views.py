from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'api/index.html')

class SearchResult(APIView):
    def get(self, request):
        # Get the search query from the 'q' URL parameter.
        query = request.GET.get('q')
        if query:
            # Call the TMDB API to search for movies with query if it exists.
            response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}')

            # Get the search results from the TMDB API response.
            results = response.json()['results']
            for result in results:
                # Call the Utelly API to get streaming information for each movie.
                response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={result["id"]}&source=tmdb', headers={'x-rapidapi-key': settings.UTELLY_API_KEY, 'x-rapidapi-host': 'utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com'})
                
                # Add the streaming information to the search result dictionary.
                result['streaming_info'] = response.json()
        else:
            # If no search query was provided, return an error message.
            return Response('Please enter a search query')
        
        # Return the search results with streaming information as a JSON response.
        return Response(results)
        

class MovieDetails(APIView):
    def get(self, request, movie_id):
        # Call the TMDB API to get the details for a specific movie
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}')
        movie = response.json()

        # Call the Utelly API to get streaming information for the movie
        response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={movie_id}&source=tmdb', headers={'x-rapidapi-key': settings.UTELLY_API_KEY, 'x-rapidapi-host': 'utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com'})
        streaming_info = response.json()

        # Return the movie details and streaming information as a JSON response.
        return Response({'movie': movie, 'streaming_info': streaming_info})


