from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("search/", views.SearchResult, name="search"),
    path("details/<int:movie_id>", views.MovieDetails, name="details"),

]
