from django.urls import path
from . import views
from .views import (
		SearchResult,
        MovieDetails
	)
urlpatterns = [
    path('', views.index, name='index'),
    path("search/", SearchResult.as_view()),
    path('movie/<int:movie_id>/', MovieDetails.as_view()),
]