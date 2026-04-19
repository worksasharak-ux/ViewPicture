from rest_framework import serializers
from .models import  *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
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

class HomePageSerializer(serializers.Serializer):
    categories = CategorySerializer(many=True)
    pictures = PictureSerializer(many=True)

