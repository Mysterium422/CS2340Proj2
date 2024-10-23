from django.shortcuts import render, redirect

# Create your views here.
def redirect_to_account(request):
    return redirect('/accounts/login')


def index(request):
    return render(request, "home/home.html", {})