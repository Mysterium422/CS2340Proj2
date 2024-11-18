from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from accounts.models import SpotifyToken
from accounts.views import refresh_spotify_token
from django.utils.timezone import now
from .spotify_api import SpotifyAPI, createWrapped
from .models import Wrapped
from django.http import JsonResponse
# Create your views here.
def redirect_to_account(request):
    if request.user.is_authenticated:
        # If the user is already logged in, redirect to the home page
        return redirect('home')
    # If the user is not logged in, redirect to the login page

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


def profile(request):
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not logged in
        return redirect(settings.LOGIN_URL)

    # Render the home page if the user is logged in
    return render(request, "home/profile.html", {"username": request.user.username})

def delete(request):
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not logged in
        return redirect(settings.LOGIN_URL)
    try:
        user = request.user
        user.delete()
    except Exception as e:
        pass
    return redirect("login")


from django.urls import reverse

def create_wrap_view(request):
    try:
        # Retrieve the user's Spotify token
        spotify_token = SpotifyToken.objects.get(user=request.user)

        # Check token expiration
        if spotify_token.expires_in <= now():
            # Handle token refresh logic (not implemented in this snippet)
            return redirect("refresh_spotify_token")

        # Instantiate the Spotify API with the user's access token
        spotify_api = SpotifyAPI(spotify_token.access_token)

        # Create the Wrapped object
        wrapped = createWrapped(request.user, spotify_api)
        # Generate the URL for the wrapped detail page
        wrapped_url = reverse('wrapped_detail', kwargs={'wrapped_id': wrapped.id})

        # Redirect to the wrapped detail page with the wrapped id in the URL
        return JsonResponse({'wrapped_url': wrapped_url})

    except SpotifyToken.DoesNotExist:
        return render(request, "error.html", {"message": "Spotify token not found."})
    
def wrapped_detail_view(request, wrapped_id):
    # Retrieve the wrapped object using the wrapped_id
    wrapped = get_object_or_404(Wrapped, id=wrapped_id)
    return render(request, 'wrapped/wrapped.html', {'wrapped': wrapped})
