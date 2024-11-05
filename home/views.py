from django.shortcuts import render, redirect
from django.conf import settings
from accounts.models import SpotifyToken

# Create your views here.
def redirect_to_account(request):
    return redirect('/accounts/login')


def index(request):
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not logged in
        return redirect(settings.LOGIN_URL)
    
    # Render the home page if the user is logged in
    print(SpotifyToken.objects.get(user=request.user).access_token)
    print("hi")
    return render(request, "home/home.html", {})