from django.shortcuts import render, redirect, reverse
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Movie, Genre, StreamInfo
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from random_word import RandomWords

#https://github.com/celiao/tmdbsimple


# Create your views here.
def index(request):
    genres = requests.get('https://api.themoviedb.org/3/genre/movie/list',
                          {'api_key': settings.TMDB_API_KEY})
    genresj = genres.json()
    genresjl = genresj['genres']
    random_query = request.session.get('random_query')
    genres = Genre.objects.values('name')
    finalgenre = []
    for genre in genres:
        finalgenre.append(genre['name'])
    print(finalgenre)
    if random_query:
        context = {'genres': finalgenre, 'random_query': random_query}
    else:
        context = {'genres': finalgenre}
    return render(request, 'api/index.html', context)


def signIn(request):
    return render(request, 'api/signIn.html')


def about(request):
    return render(request, 'api/about.html')


# Pre-Load the movie genres from API to database
def loadGenres():
    genres = requests.get('https://api.themoviedb.org/3/genre/movie/list',
                          {'api_key': settings.TMDB_API_KEY})
    genresj = genres.json()
    genresjl = genresj['genres']
    for genre in genresjl:
        id = genre['id']
        name = genre['name']
        Genre.objects.get_or_create(gid=id, name=name)


def SearchResult(request):
    loadGenres()
    # Get the search query from the 'q' URL parameter.
    query = request.GET.get('q')
    if query:
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': settings.TMDB_API_KEY,
            'query': query,
        }
        # Call the TMDB API to search for movies with query if it exists.
        response = requests.get(url, params=params)
        results = response.json()['results']
        with_genres = request.GET.get(
            'with_genres',
            '28,12,16,35,80,99,19751,14,36,27,10402,9648,10749,878,10770,53,10752,37'
        )
        with_genres = [int(s) for s in with_genres.split(",")]
        # Insert the movies queried into the database
        finalresult = []
        for movie in results:
            # print(movie['genre_ids'])
            if any(genre_id in movie['genre_ids'] for genre_id in with_genres):
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
                if (len(release) != 10):
                    release = None

                Movie.objects.get_or_create(id=id,
                                            defaults={
                                                "poster_path": posterpath,
                                                "backdrop_path": backdroppath,
                                                "adult": adult,
                                                "release_date": release,
                                                "original_language":
                                                oglanguage,
                                                "original_title": ogtitle,
                                                "overview": overview,
                                                "title": title,
                                                "video": video
                                            })
                d2 = Movie.objects.get(id=id)

                ## Assigning each movies its genres

                for genre in genres:
                    d2.genres.add(genre)

                ##print(d2.__dict__) to see fields
                ##Checking if genres worked
                #for genre in d2.genres.all():
                #print(genre.__dict__)
                finalresult.append(d2)

        for result in results:
            if any(genre_id in result['genre_ids']
                   for genre_id in with_genres):
                # Call the Utelly API to get streaming information for each movie.
                response = requests.get(
                    f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={result["id"]}&source=tmdb',
                    headers={
                        'x-rapidapi-key': settings.X_RAPIDAPI_KEY,
                        'x-rapidapi-host': settings.X_RAPIDAPI_HOST
                    })
                id = result['id']

                d2 = Movie.objects.get(id=id)
                # Add the streaming information to the search result dictionary.
                result['streaming_info'] = response.json()['collection']
                if (result['streaming_info']):
                    xd = result['streaming_info']['locations']
                    for x in xd:
                        displayn = x['display_name']
                        sid = x['id']
                        url = x['url']
                        name = x['name']
                        icon = x['icon']
                        ## Inserting the streaming info for each movie
                        newinfo = StreamInfo.objects.get_or_create(
                            display_name=displayn,
                            sid=sid,
                            url=url,
                            name=name,
                            icon=icon)
                        d2.streaminfo.add(newinfo[0].id)
                ##Just some checking
                ##for genre in d2.streaminfo.all():
                ##print(genre.__dict__)

    else:
        # If no search query was provided, return an error message.
        return HttpResponse('Please enter a search query')
    genres = Genre.objects.values('name')
    finalgenre = []
    for genre in genres:
        finalgenre.append(genre['name'])
    context = {'results': finalresult, 'genres': finalgenre}
    return render(request, 'api/results.html', context)
    # Return the search results with streaming information as a JSON response.


def MovieDetails(request, movie_id):  # Get imdb id using TMDB API
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}/external_ids?api_key={settings.TMDB_API_KEY}'
    )
    imdb_id = response.json()['imdb_id']

    # If imdb id exists, redirect to IMDb page
    if imdb_id:
        response = requests.get(
            f'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup?country=us&source_id={imdb_id}&source=imdb',
            headers={
                'x-rapidapi-key': settings.X_RAPIDAPI_KEY,
                'x-rapidapi-host': settings.X_RAPIDAPI_HOST
            })
        imdb_url = response.json()['collection']['source_ids']['imdb']['url']
        return redirect(imdb_url)

    return redirect(request.path_info)


def random_query(request):
    r = RandomWords()
    random_query = r.get_random_word()
    context = {'random_query': random_query}
    # request.session['random_query'] = random_query
    # return redirect(index)
    return HttpResponse(random_query)