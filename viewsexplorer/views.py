from email.iterators import typed_subpart_iterator

from django.contrib.auth import logout
from django.shortcuts import render, redirect
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

    @action(methods=['post'], detail=False, url_path='addpicture')
    def addpicture(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            serializer = PictureSerializer(data={
                "title": request.data['title'],
                "author": user_profile.id,
                "image": request.FILES['image'],
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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



    @action(methods=['post'], detail=False, url_path='logout')
    def logout(self, request):
        logout(request)
        print(request.user.is_authenticated)
        if request.accepted_renderer.format == 'html':
            return redirect("/api/home")
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )





class PostsViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Если клиент просит HTML (через заголовок Accept или расширение .html)
        if request.accepted_renderer.format == 'html':
            # print(serializer.data)
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
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'createpost.html'

    def list(self, request):
        """Отображение HTML страницы с формой"""
        return Response({}, template_name=self.template_name)

    @action(methods=['post'], detail=False, url_path='addpost', renderer_classes=[JSONRenderer])
    def addpost(self, request):
        user_profile = UserProfile.objects.filter(user=request.user).first()

        if not user_profile:
            return Response(
                {"error": "Профиль пользователя не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        title = request.data.get('title')
        if not title:
            return Response(
                {"error": "Название поста обязательно"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаём пост
        post = Post.objects.create(
            title=title,
            author=user_profile,
            created_at=datetime.datetime.now(),
        )

        # Добавляем картинки
        picture_ids = request.data.get('pictures', [])
        if picture_ids:
            pictures = Picture.objects.filter(id__in=picture_ids)
            post.pictures.set(pictures)

        # Формируем ответ
        return Response({
            "id": post.id,
            "title": post.title,
            "author": str(user_profile),
            "pictures": [p.id for p in post.pictures.all()],
            "created_at": post.created_at
        }, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='getpictures',renderer_classes=[JSONRenderer])
    def getpictures(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            pictures = Picture.objects.filter(author=user_profile)
            serializer = PictureSerializer(pictures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)