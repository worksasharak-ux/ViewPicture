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

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author','author_name', 'text', 'created_at', 'picture']
        read_only_fields = ['id', 'created_at', 'author_name']
        extra_kwargs = {
            'post': {'required': True},
            'author': {'required': False, 'allow_null': True}
        }

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_username()
        return 'anonymous'

class PostSerializer(serializers.ModelSerializer):
    picture_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Picture.objects.all(),
        write_only=True,
        required=False,
        source='pictures' # Сохраняется в поле pictures
    )

    pictures = PictureSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'author','author_name', 'pictures', 'picture_ids', 'comments', 'created_at']
        read_only_fields = ['id', 'created_at', 'author_name']
        extra_kwargs = {
            'author': {'required': False},
            'comments': {'required': False, 'allow_null': True}
        }

    def get_author_name(self, obj):
        return obj.author.get_username()

class UserProfileSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'