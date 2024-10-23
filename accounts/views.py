from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.utils import timezone
import datetime
import requests
from .models import SpotifyToken
# Create your views here.
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.signals import user_logged_in

from urllib.parse import urlencode
spotify_api_key = settings.SPOTIFY_WEB_API_KEY
spotify_redirect_uri = settings.SPOTIFY_REDIRECT_URI
spotify_client_secret = settings.SPOTIFY_CLIENT_SECRET
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Save the new user
        user = form.save()
        # Automatically log in the new user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')  # Use the password they just set
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)  # Log in the user
        return redirect('spotify_login')
#defined things to obtain from user
SPOTIFY_SCOPES = 'user-top-read user-read-email'
def spotify_login(request):
    params = {
        'client_id': spotify_api_key,
        'response_type': 'code',
        'redirect_uri': spotify_redirect_uri,
        'scope': SPOTIFY_SCOPES,
        'show_dialog': 'true',
    }
    print("Redirect URI: ", params['redirect_uri']) 
    spotify_auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
    return redirect(spotify_auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    
    # Exchange the code for an access token and refresh token
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': spotify_redirect_uri,
        'client_id': spotify_api_key,
        'client_secret': spotify_client_secret
    })
    
    response_data = response.json()
    access_token = response_data.get('access_token')
    refresh_token = response_data.get('refresh_token')
    expires_in = response_data.get('expires_in')
    
    # Calculate when the access token will expire
    expires_at = timezone.now() + datetime.timedelta(seconds=expires_in)
    
    # Save the tokens to the user's account
    user = request.user
    SpotifyToken.objects.update_or_create(
        user=user,
        defaults={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_at
        }
    )
    
    # Redirect to home or a dashboard
    return redirect('home')

@receiver(user_logged_in)
def link_spotify_on_login(sender, request, user, **kwargs):
    """
    Automatically check if Spotify tokens are present and link the Spotify account after login.
    """
    try:
        # Check if Spotify tokens already exist for this user
        token = SpotifyToken.objects.get(user=user)
        print("Spotify tokens found for user:", user.username);
        if token.expires_in < timezone.now():
            # Refresh the Spotify token if it's expired
            refresh_spotify_token(user)
    except SpotifyToken.DoesNotExist:
        # If no Spotify token is found, redirect the user to the Spotify OAuth flow
        params = {
            'client_id': spotify_api_key,
            'response_type': 'code',
            'redirect_uri': spotify_redirect_uri,
            'scope': SPOTIFY_SCOPES,
            'show_dialog': 'true',
        }
        spotify_auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
        return redirect(spotify_auth_url)
    
def refresh_spotify_token(user):
    try:
        token = SpotifyToken.objects.get(user=user)
        if token.expires_in < timezone.now():
            # Token expired, refresh it
            response = requests.post('https://accounts.spotify.com/api/token', data={
                'grant_type': 'refresh_token',
                'refresh_token': token.refresh_token,
                'client_id': spotify_api_key,
                'client_secret': spotify_client_secret
            })
            
            response_data = response.json()
            new_access_token = response_data.get('access_token')
            expires_in = response_data.get('expires_in')
            token.access_token = new_access_token
            token.expires_in = timezone.now() + datetime.timedelta(seconds=expires_in)
            token.save()
    except SpotifyToken.DoesNotExist:
        # Handle case where no token exists
        pass