from django.urls import path
from . import views

app_name = "pages" 

urlpatterns = [
    path("getting-started_driver/", views.getting_started_driver, name="getting_started_driver"),
    path("getting-started_commuter/", views.getting_started_commuter, name="getting_started_commuter"),
    path("routes/", views.routes_page, name="routes"),
]