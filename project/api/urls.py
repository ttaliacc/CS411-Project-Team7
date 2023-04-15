from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("search/", , name="search"),
    path('search/', views.get_search_result, name='search_results'),
    path('details/<int:movie_id>/', views.get_movie_detail, name='movie_details'),
]
