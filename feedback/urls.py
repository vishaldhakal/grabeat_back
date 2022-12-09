from django.urls import path, include
from .views import feedback

urlpatterns = [
    path("", feedback),
]
