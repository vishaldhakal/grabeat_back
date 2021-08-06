from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import foodlists, submitcart,orderslists

urlpatterns = [
    path("foodlists/", foodlists),
    path("orderslists/", orderslists),
    path("submitcart/", submitcart),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
