"""
Views for the Spotify Wrapped app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from accounts.models import SpotifyToken
from accounts.views import refresh_spotify_token
from home.spotify_api import SpotifyAPI, create_wrapped
from home.models import Wrapped
# Create your views here.

def check_authenticated(request):
    """
    Check if the user is authenticated
    """
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    return None


def redirect_to_account(request):
    """
    Redirect to the account page
    """
    redirect_response = check_authenticated(request)
    if redirect_response:
        return redirect_response
    wraps = Wrapped.objects.filter(user=request.user).order_by('-date')
    refresh_spotify_token(request.user)
    print(len(wraps))
    return render(request, "home/home.html", {'wraps': wraps})

def index(request):
    """
    Index view
    """
    redirect_response = check_authenticated(request)
    if redirect_response:
        return redirect_response
    wraps = Wrapped.objects.filter(user=request.user).order_by('-date')
    refresh_spotify_token(request.user)
    print(len(wraps))
    return render(request, "home/home.html", {'wraps': wraps})

def profile(request):
    """
    Profile view
    """
    redirect_response = check_authenticated(request)
    if redirect_response:
        return redirect_response

    return render(request, "home/profile.html", {"username": request.user.username})


def delete(request):
    """
    Delete user view
    """
    redirect_response = check_authenticated(request)
    if redirect_response:
        return redirect_response

    try:
        user = request.user
        user.delete()
    except Exception as _e:
        pass
    return redirect("login")

def create_wrap_view(request):
    """
    Create a wrapped view
    """
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
        wrapped = create_wrapped(request.user, spotify_api)
        # Generate the URL for the wrapped detail page
        wrapped_url = reverse('wrapped_detail', kwargs={'wrapped_id': wrapped.id})

        # Redirect to the wrapped detail page with the wrapped id in the URL
        return JsonResponse({'wrapped_url': wrapped_url})

    except SpotifyToken.DoesNotExist:
        return render(request, "error.html", {"message": "Spotify token not found."})

def wrapped_detail_view(request, wrapped_id):
    """
    View wrapped detail view
    """
    # Retrieve the wrapped object using the wrapped_id
    wrapped = get_object_or_404(Wrapped, id=wrapped_id)
    top_songs = wrapped.top_songs.through.objects.filter(wrapped=wrapped).order_by('rank')
    top_weekly_songs = wrapped.top_weekly_songs.through.objects.filter(
        wrapped=wrapped
        ).order_by('rank')
    top_artists = wrapped.top_artists.through.objects.filter(
        wrapped=wrapped
        ).order_by('rank')
    top_weekly_artists = wrapped.top_weekly_artists.through.objects.filter(
        wrapped=wrapped
        ).order_by('rank')

    context = {
        'wrapped': wrapped,
        'top_songs': top_songs,
        'top_weekly_songs': top_weekly_songs,
        'top_artists': top_artists,
        'top_weekly_artists': top_weekly_artists,
        'recommended_songs': wrapped.recomended_songs.all(),
    }
    return render(request, 'home/wrapped.html', context)

@login_required
def delete_wrap(request, wrap_id):
    """
    Delete wrap view
    """
    if request.method == 'DELETE':
        wrap = get_object_or_404(Wrapped, id=wrap_id, user=request.user)
        wrap.delete()
        return JsonResponse({'message': 'Wrap deleted successfully!'}, status=200)
    return HttpResponseForbidden("You are not allowed to perform this action.")
