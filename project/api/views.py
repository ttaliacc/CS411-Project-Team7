from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Movie, Genre, StreamInfo, FavoritedMovie
from django.core.serializers import serialize
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


#https://github.com/celiao/tmdbsimple

# Create your views here.
def index(request):
    genres = requests.get('https://api.themoviedb.org/3/genre/movie/list',
    {'api_key' : settings.TMDB_API_KEY}) 
    genresj = genres.json()
    genresjl = genresj['genres']
    context = {genres:genresjl} 
    print(context)
    return render(request, 'api/index.html', context)

def signIn(request):
    return render(request, 'api/signIn.html')

def about(request):
    return render(request, 'api/about.html')


# Pre-Load the movie genres from API to database
def loadGenres():
    genres = requests.get('https://api.themoviedb.org/3/genre/movie/list',{'api_key' : settings.TMDB_API_KEY})    
    genresj = genres.json()
    genresjl = genresj['genres']
    for genre in genresjl:
        id = genre['id']
        name = genre['name']
        Genre.objects.get_or_create(gid=id,name=name)

def SearchResult(request):
    loadGenres()
    # Get the search query from the 'q' URL parameter.
    query = request.GET.get('q')
    if query:
        squery = request.GET.get('q')
    if query:
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
        'api_key': settings.TMDB_API_KEY,
        'query': query
        }  
        # Call the TMDB API to search for movies with query if it exists.
        response = requests.get(url, params=params)
        results = response.json()['results']

        # Insert the movies queried into the database
        finalresult = []
        for movie in results:
            id = movie['id'] 
            adult = movie['adult']
            oglanguage = movie['original_language']
            ogtitle = movie['original_title']
            overview = movie['overview']
            title = movie['title']
            video = movie['video']
            release = movie['release_date']
            genres = movie['genre_ids']
            posterpath = movie['poster_path']
            backdroppath = movie['backdrop_path']

            ## INSERT INTO Movies
            if(len(release) != 10) :
                release = None
            
            Movie.objects.get_or_create(id = id,defaults={"poster_path":posterpath, "backdrop_path":backdroppath, "adult" : adult,"release_date":release, "original_language":  oglanguage, "original_title" : ogtitle, "overview":overview, "title":title, "video":video}) 
            d2 = Movie.objects.get(id=id)

            
            ## Assigning each movies its genres 
            for genre in genres:
                d2.genres.add(genre)


            ##print(d2.__dict__) to see fields
            ##Checking if genres worked
            ##for genre in d2.genres.all():
                   ##print(genre.__dict__)
            finalresult.append(d2)
        
        for result in results:
            # Call the Utelly API to get streaming information for each movie.
            response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={result["id"]}&source=tmdb', headers={'x-rapidapi-key': settings.X_RAPIDAPI_KEY, 'x-rapidapi-host': settings.X_RAPIDAPI_HOST})
            id = result['id']
            d2 = Movie.objects.get(id=id) 
            # Add the streaming information to the search result dictionary.
            result['streaming_info'] = response.json()['collection']
            if(result['streaming_info']):
                xd=result['streaming_info']['locations']
                for x in xd:
                    displayn = x['display_name']
                    sid = x['id']
                    url = x['url']
                    name = x['name']
                    icon = x['icon']
                    ## Inserting the streaming info for each movie
                    newinfo = StreamInfo.objects.get_or_create(display_name=displayn,sid=sid,url=url,name=name,icon=icon)
                    d2.streaminfo.add(newinfo[0].id)
            ##Just some checking
            ##for genre in d2.streaminfo.all():
                ##print(genre.__dict__)
        

    else:
        # If no search query was provided, return an error message.
        return HttpResponse('Please enter a search query')
    context = {'results': finalresult}
    return render(request, 'api/results.html', context)
    # Return the search results with streaming information as a JSON response.

#Currently not supported
def MovieDetail(request, movie_id):

    # Get imdb id using TMDB API
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/external_ids?api_key={settings.TMDB_API_KEY}')
    imdb_id = response.json()['imdb_id']

    # If imdb id exists, redirect to IMDb page
    if imdb_id:
        response = requests.get(f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={imdb_id}&source=imdb', headers={'x-rapidapi-key': settings.X_RAPIDAPI_KEY, 'x-rapidapi-host': settings.X_RAPIDAPI_HOST})  
        imdb_url = response.json()['collection']['source_ids']['imdb']['url']
        return redirect(imdb_url)

    return HttpResponse('Movie not found in IMDb')

#Needs Work 
@login_required
class FavoriteMovie(ListView):
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            favorites = FavoritedMovie.objects.filter(user=self.request.user)
            context['favorites_movie_id'] = [favorite.movie_id for favorite in favorites]
            return context

    def get_favorite_movies(self):
        return FavoritedMovie.objects.filter(user=self.request.user)


    def add_delete(request, movie_id):
        favorites = FavoritedMovie.objects.filter(user=request.user, movie_id=movie_id)
        is_favorited = True if favorites else False

        if request.method == 'POST':
            if 'add' in request.POST:
                if not is_favorited:
                    favorite = FavoritedMovie(user=request.user, movie_id=movie_id)
                    favorite.save()
                    return HttpResponseRedirect(request.path_info)
                else:            
                    return HttpResponse('Movie already in favorites') 
            if 'remove' in request.POST:
                favorites.delete()
                return HttpResponseRedirect(request.path_info)


        context = {
            'movie_id': movie_id,
            'is_favorite': is_favorited
        }
        return render(request, 'movie_detail.html', context)



