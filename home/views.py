from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
def redirect_to_account(request):
    return redirect('/accounts/login')


def index(request):
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not logged in
        return redirect(settings.LOGIN_URL)
    
    # Render the home page if the user is logged in
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
