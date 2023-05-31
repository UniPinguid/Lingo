from django.shortcuts import render
from django.http import HttpResponse

# Main screens
def home(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'pages/signup.html')

def signin(request):
    return render(request, 'pages/signin.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')

# Project subscreens

def project(request):
    return render(request, 'pages/project/main.html')

def members(request):
    return render(request, 'pages/project/members.html')

def tasks(request):
    return render(request, 'pages/project/tasks.html')

def labels(request):
    return render(request, 'pages/project/labels.html')

def contribution(request):
    return render(request, 'pages/project/contribution.html')