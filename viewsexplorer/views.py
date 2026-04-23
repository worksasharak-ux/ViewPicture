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

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class TestViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Если клиент просит HTML (через заголовок Accept или расширение .html)
        if request.accepted_renderer.format == 'html':
            #print(serializer.data)
            return Response(
                {
                    'profiles': serializer.data
                },
                template_name='home.html'
            )
        return Response(serializer.data)
