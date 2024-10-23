from django.urls import path

from .views import SignUpView, spotify_login, spotify_callback


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('spotify/login/', spotify_login, name='spotify_login'),
    path('spotify/callback/', spotify_callback, name='spotify_callback'),

]