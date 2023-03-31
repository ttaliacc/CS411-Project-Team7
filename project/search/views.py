from django.shortcuts import render
import requests

def search_movies(request):
    # Get the user's search query from the request
    query = request.GET.get('q')

    # Construct the search request to the API
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': '3016e6c23565d0fd1b4b0e0953da86d2',
        'query': query
    }

    # Make the request to the API and get the response
    response = requests.get(url, params=params)

    # Extract the relevant information from the response
    results = []
    if response.status_code == 200:
        data = response.json()
        for movie in data['results']:
            results.append({
                'title': movie['title'],
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            })

    # Render the template with the search results
    return render(request, 'search_results.html', {'results': results})
