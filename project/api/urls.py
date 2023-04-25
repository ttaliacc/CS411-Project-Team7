from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("search/", views.SearchResult, name="search"),
    path("random_query/", views.random_query, name="random_query"),
    path("details/<int:movie_id>/", views.MovieDetails, name="details"),
    path("signIn/", views.signIn, name="signIn"),
    path("about/", views.about, name="about"),


]
