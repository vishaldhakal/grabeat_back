from django.urls import path, include
from .views import userlists

urlpatterns = [
    path("users/", userlists),
]
