from djoser.serializers import UserSerializer as djoser_UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


# initialize the shown fields of UserSerializer of djoser
djoser_UserSerializer.Meta.fields = ["first_name", "last_name", "username", "email"]
djoser_UserSerializer.Meta.read_only_fields += ('created_at',)


class CurrentUserSerializer(djoser_UserSerializer):
    class Meta(djoser_UserSerializer.Meta):
        fields = ["first_name", "last_name", "username", "email", "created_at", "is_seller", "is_staff"]
        read_only_fields = djoser_UserSerializer.Meta.read_only_fields + ('created_at',)