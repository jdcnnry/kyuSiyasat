from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def getting_started_driver(request):
    return render(request, 'pages/getting_started_driver.html')

@login_required
def getting_started_commuter(request):
    return render(request, 'pages/getting_started_commuter.html')

@login_required
def routes_page(request):
    return render(request, 'pages/routes.html')
