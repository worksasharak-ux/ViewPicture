from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .models import *
from .serializer import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs): # переопределяем queryset
        self.queryset = self.queryset.filter()

        return super().list(request, *args, **kwargs)

class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TestViewSet(viewsets.ViewSet):
    #renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    def list(self, request):
        categories = Category.objects.all()
        pictures = Picture.objects.all()
        data = {
            'categories': categories,
            'pictures': pictures,
        }
        serializer = HomePageSerializer(data)
        return Response(serializer.data)
