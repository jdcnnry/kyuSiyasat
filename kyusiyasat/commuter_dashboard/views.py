from django.shortcuts import render

# Create your views here.
def commuter_dashboard(request):
    return render(request, 'commuter_dashboard.html', {'user': request.user})