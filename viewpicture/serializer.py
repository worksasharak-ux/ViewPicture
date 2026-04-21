from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from viewsexplorer.models import UserProfile

user = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = user
        fields = ('username', 'password')

    def create(self, validated_data):
        tempuser = user.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        prof, created = UserProfile.objects.get_or_create(user=tempuser)
        #print(prof.get_username())
        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Необходимо ввести логин и/или пароль")
        else:
            user_obj = authenticate(username=username, password=password)
            if not user_obj:
                raise serializers.ValidationError("Неверный логин или пароль")

        data['user'] = user_obj
        #print(user_obj.get_username())
        return data
