from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def home(request):
    print("In home World")
    return render(request, 'info/home.html')

def about(request):
    print("In about")
    return render(request, 'info/about.html')

def contact(request):
    print("In contact")
    return render(request, 'info/contact.html')

def blog(request):
    print("In blog World")
    return render(request, 'info/blog.html')
