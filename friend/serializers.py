from django.contrib.auth import get_user_model
from rest_framework import serializers


class FriendSerializer(serializers.ModelSerializer):

    color = serializers.CharField(source="avatar.color")
    image = serializers.FileField(source="avatar.image")

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "color", "image"]
