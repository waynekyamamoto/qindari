from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    print("In profile")
    return render(request, 'user/profile.html')

@login_required
def dashboard(request):
    print("In dashboard")
    return render(request, 'user/dashboard.html')
