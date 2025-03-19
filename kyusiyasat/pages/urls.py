from django.urls import path
from .views import getting_started_commuter, getting_started_driver, routes_page

app_name = "pages" 

urlpatterns = [
    path("getting-started_driver/", getting_started_driver, name="getting_started_driver"),
    path("getting-started_commuter/", getting_started_commuter, name="getting_started_commuter"),
    path("routes/", routes_page, name="routes"),
]