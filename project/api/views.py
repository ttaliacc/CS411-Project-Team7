from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import ListView
from .models import FavoriteMovies
from django.contrib.auth.decorators import login_required
import tmdbsimple as tmdb
tmdb.API_KEY = settings.TMDB_API_KEY

# Create your views here.
def index(request):
    return render(request, 'api/index.html')

def get_stream_info(movie_id):
    response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={movie_id}&source=tmdb', headers={'x-rapidapi-key': settings.X_RAPIDAPI_KEY, 'x-rapidapi-host': 'utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com'})
    stream_info = response.json()['collection']
    return stream_info

def get_recommended(movie_id):
    return requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={settings.TMDB_API_KEY}&language=en-US&page=1').json()

# def get_movie_info(movie_id):
#     return requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}').json()

def signIn(request):
    return render(request, 'api/signIn.html')

def about(request):
    return render(request, 'api/about.html')

def get_search_result(request):
    # Get the search query from the 'q' URL parameter.
    query = request.GET.get('q')

    if query:
        # Call the TMDB API to search for movies with query if it exists.
        search = tmdb.Search()
        response = search.movie(query=query)
        results = search.results
        # Get the search results from the TMDB API response.
        for result in results:
            print(type(result))
            # Call the Utelly API to get streaming information for each movie.
            # Add the streaming information to the search result dictionary.
            result['stream_info'] = get_stream_info(result['id'])
    else:
        # If no search query was provided, return an error message.
        return HttpResponse('Please enter a search query')
    
    context = {'results': results}

    return render(request,'api/results.html', context)
 
def get_movie_detail(request, movie_id):
    # Call the TMDB API to get the details for a specific movie
    movie = tmdb.Movies(movie_id)
    movie_info = movie.info()
    recommendations = movie.recommendations()
    stream_info = get_stream_info(movie_id)
    context = {'movie_info': movie_info,
               'stream_info': stream_info, 
               'recommendations': recommendations}
    return JsonResponse(context)
    # return render(request, 'api/movie_detail.html', context)


@login_required
class FavoriteMovie(ListView):
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            favorites = FavoriteMovies.objects.filter(user=self.request.user)
            context['favorites_movie_id'] = [favorite.movie_id for favorite in favorites]
            return context

    def get_favorite_movies(self):
        return FavoriteMovies.objects.filter(user=self.request.user)

    
    def add_to_favorites(self, movie_id):
        if FavoriteMovies.objects.filter(movie_id=movie_id).exists():
            return HttpResponse('Movie already in favorites')  
        favorite = FavoriteMovies.objects.add(movie_id=movie_id)

    def add_delete(request, movie_id):
        favorites = FavoriteMovies.objects.filter(user=request.user, movie_id=movie_id)
        is_favorited = True if favorites else False

        if request.method == 'POST':
            if 'add' in request.POST:
                if not is_favorited:
                    favorite = FavoriteMovies(user=request.user, movie_id=movie_id)
                    favorite.save()
                    return HttpResponseRedirect(request.path_info)
            if 'remove' in request.POST:
                favorites.delete()
                return HttpResponseRedirect(request.path_info)


        context = {
            'movie_id': movie_id,
            'is_favorite': is_favorited
        }
        return render(request, 'movie_detail.html', context)

