from django.shortcuts import render, redirect
from django.conf import settings
from accounts.models import SpotifyToken
from accounts.views import refresh_spotify_token

# Create your views here.
def redirect_to_account(request):
    return redirect('/accounts/login')


def index(request):
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not logged in
        return redirect(settings.LOGIN_URL)
    
    # Render the home page if the user is logged in
    refresh_spotify_token(request.user)
    print(SpotifyToken.objects.get(user=request.user).access_token)
    print(refresh_spotify_token(request.user))
    return render(request, "home/home.html", {})