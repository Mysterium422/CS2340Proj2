from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm


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
        return redirect("/home/")