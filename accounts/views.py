"""
Views for the accounts app.
"""

from urllib.parse import urlencode
import datetime
import requests

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from django.contrib.auth.signals import user_logged_in


from accounts.models import SpotifyToken
from accounts.forms import CustomUserCreationForm

spotify_api_key = settings.SPOTIFY_WEB_API_KEY
spotify_redirect_uri = settings.SPOTIFY_REDIRECT_URI
spotify_client_secret = settings.SPOTIFY_CLIENT_SECRET

class SignUpView(CreateView):
    """
    Sign Up View
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("")
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches signup view 
        """
        # Redirect to home if the user is already logged in
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Form validator
        """
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
SPOTIFY_SCOPES = 'user-top-read user-read-email user-read-recently-played user-top-read'

def spotify_login(_request):
    """
    Login user into spotify
    """
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
    """
    Spotify login callback
    """
    code = request.GET.get('code')
    tokens = exchange_code_for_tokens(code)
    save_spotify_tokens(request.user, tokens)
    return redirect('home')

def exchange_code_for_tokens(code):
    """
    Exchange code for tokens
    """
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': spotify_redirect_uri,
        'client_id': spotify_api_key,
        'client_secret': spotify_client_secret,
    }, timeout=30)
    response_data = response.json()
    return {
        'access_token': response_data.get('access_token'),
        'refresh_token': response_data.get('refresh_token'),
        'expires_in': response_data.get('expires_in')
    }

def save_spotify_tokens(user, tokens):
    """
    Save Spotify tokenss
    """
    expires_at = timezone.now() + datetime.timedelta(seconds=tokens['expires_in'])
    SpotifyToken.objects.update_or_create(
        user=user,
        defaults={
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'expires_in': expires_at
        }
    )

@receiver(user_logged_in)
def link_spotify_on_login(sender, request, user, **_kwargs):
    """
    Automatically check if Spotify tokens are present and link the Spotify account after login.
    """
    print(sender)
    print(request)
    try:
        # Check if Spotify tokens already exist for this user
        token = SpotifyToken.objects.get(user=user)
        print("Spotify tokens found for user:", user.username)
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
    return None

def refresh_spotify_token(user):
    """
    Refresh Spotify token
    """
    try:
        token = SpotifyToken.objects.get(user=user)
        if token.expires_in < timezone.now():
            # Token expired, refresh it
            response = requests.post('https://accounts.spotify.com/api/token', data={
                'grant_type': 'refresh_token',
                'refresh_token': token.refresh_token,
                'client_id': spotify_api_key,
                'client_secret': spotify_client_secret,
            }, timeout=30)
            response_data = response.json()
            new_access_token = response_data.get('access_token')
            expires_in = response_data.get('expires_in')
            token.access_token = new_access_token
            token.expires_in = timezone.now() + datetime.timedelta(seconds=expires_in)
            token.save()
    except SpotifyToken.DoesNotExist:
        # Handle case where no token exists
        pass

def redirect_to_home(_request):
    """
    Redirect to home
    """
    return redirect('/home/')
