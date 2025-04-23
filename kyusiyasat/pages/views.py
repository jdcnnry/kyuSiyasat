from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def getting_started_driver(request):
    request.user.profile.has_seen_getting_started = True
    request.user.profile.save()
    
    return render(request, 'getting_started_driver.html')

@login_required
def getting_started_commuter(request):
    request.user.profile.has_seen_getting_started = True
    request.user.profile.save()

    return render(request, 'getting_started_commuter.html')

@login_required
def routes_page(request):
    return render(request, 'routes.html')