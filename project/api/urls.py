from django.urls import path
from . import views
from .views import (
		SearchResult,
        MovieDetails
	)
urlpatterns = [
    path("search/<query>", SearchResult.as_view(), name='search'),
    path('details/<int:movie_id>/', MovieDetails.as_view(), name='movie_details'),
]