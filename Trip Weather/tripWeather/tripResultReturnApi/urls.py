from django.urls import path
from tripResultReturnApi import views

#url patterns to make the exposed API's accessible for use in the application

urlpatterns = [
    #path to feth trip data for a specific trip
    path("api-data/get/<str:trip>", views.readTripWeather.as_view(), name="trip-weather-info"),
    #path to post data, used to add new trips into the system
    path("api-data/post/", views.tripWeatherRetrieveUpdateDestroy.as_view(), name="postTrip1"),
    #path to create a new city this used to add new data by passing only certain parameters into the system
    path("api-data/createnewtrip/<str:tripinfo>", views.tripWeatherPostTrip.as_view(), name="postTrip3")
]