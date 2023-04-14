from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("search/", , name="search"),
    path('search/', views.SearchResult, name='results'),
    path('details/<int:movie_id>/', views.MovieDetail, name='movie_details'),
]
