from django.shortcuts import render, redirect
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
def login(request):
    user_email = request.user.email
    return render(request, 'user/login.html', {'user_email':user_email})
    
def logout_view(request):
    logout(request)
    return redirect('/')

