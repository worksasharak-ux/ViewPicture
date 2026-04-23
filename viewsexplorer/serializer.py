from rest_framework import serializers
from rest_framework.response import Response

from .models import  *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Picture
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

