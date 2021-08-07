from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    foodlists,
    submitcart,
    orderslists,
    ads,
    categorylists,
    foodlists_search,
)

urlpatterns = [
    path("foodlists/", foodlists),
    path("foodlists_search/", foodlists_search),
    path("categorylists/", categorylists),
    path("ads/", ads),
    path("orderslists/", orderslists),
    path("submitcart/", submitcart),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
