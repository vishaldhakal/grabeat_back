from rest_framework import serializers
from . import models
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User
        depth = 1
