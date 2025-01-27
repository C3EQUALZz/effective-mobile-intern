from django.urls import path

from dogs.application.api.v1.api import api


urlpatterns = [
    path("v1/", api.urls),
]
