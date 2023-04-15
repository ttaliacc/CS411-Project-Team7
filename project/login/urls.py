from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='index'),
    path('logout/', views.logout_view, name='logout'),
]