"""
View for the wrapped page
"""

from django.shortcuts import render, redirect
from django.conf import settings

def wrapped(request):
    """
    Get view for the wrapped page
    """
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not logged in
        return redirect(settings.LOGIN_URL)

    # Render the home page if the user is logged in
    return render(request, "wrapped/wrapped.html", {})
