from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
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

class UserProfileViewSet(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'profile.html'

    def list(self, request):
        if request.user.is_authenticated:
            queryset = UserProfile.objects.filter(user=request.user).first()
            serializer = self.get_serializer(queryset, many=False)# если мэни фолс - то будет не список объектов

            if request.accepted_renderer.format == 'html':
                #print(serializer.data)
                return Response(
                    {
                        "data": serializer.data,
                        "username": queryset.get_username(),
                    }
                )

            return Response(serializer.data)
        else:
            return Response(
                {
                    "error": "unauthorized",
                    "message": "Пожалуйста, авторизуйтесь",
                    "redirect_url": "login/",  # Клиент сам решит, как использовать этот URL
                    "requires_auth": True
                },
                status=status.HTTP_401_UNAUTHORIZED,
                template_name='profile.html'
            )

    def logout(self, request):
        user_profile = UserProfile.objects.filter(user=request.user).first()





class PostsViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Если клиент просит HTML (через заголовок Accept или расширение .html)
        if request.accepted_renderer.format == 'html':
            #print(serializer.data)
            return Response(
                {
                    'posts': serializer.data
                },
                template_name='home.html'
            )
        return Response(serializer.data)






class CreatePostViewSet(viewsets.GenericViewSet): # пока не отрабатывает
    queryset = Post.objects.all()
    serializer_class = PostSerializer