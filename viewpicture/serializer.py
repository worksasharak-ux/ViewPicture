from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response

user = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = user
        fields = ('username', 'password')

    def create(self, validated_data):
        user.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
