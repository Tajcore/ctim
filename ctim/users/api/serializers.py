# ctim/ctim/users/api/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ctim.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["name", "url", "business_role", "company", "industry", "interests"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
