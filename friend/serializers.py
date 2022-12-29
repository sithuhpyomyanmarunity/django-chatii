from django.contrib.auth import get_user_model
from rest_framework import serializers


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["pk", "username", "first_name", "last_name"]
