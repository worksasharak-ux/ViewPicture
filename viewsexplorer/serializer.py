import datetime

from django.db.models.signals import post_init
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

    # def create(self, validated_data):
    #     picture = Picture.objects.create(
    #         title=validated_data['title'],
    #         author=validated_data['author'],
    #         image=validated_data['image'],
    #         created_at=datetime.datetime.now(),
    #     )
    #     return picture

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at', 'picture']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'post': {'required': True},
            'author': {'required': False, 'allow_null': True}
        }

class PostSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

    # def create(self, validated_data): #создание поста
    #     post = Post.objects.create(
    #         title=validated_data['title'],
    #         created_at=datetime.datetime.now(),
    #         author=validated_data['author'],
    #         pictures=validated_data['pictures'],
    #     )
    #
    #     return post



class UserProfileSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

