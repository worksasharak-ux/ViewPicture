from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

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
                #if serializer.data is not None:
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
                    "message_url": "Перейти к странице входа",
                    "requires_auth": True
                },
                status=status.HTTP_401_UNAUTHORIZED,
                template_name='profile.html'
            )

    @action(methods=['post'], detail=False, url_path='addpicture')
    def addpicture(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if 'image' not in request.FILES or 'title' not in request.data:
                return Response(
                    {
                        "error": "Values must not be empty",
                        "message": "Нужно заполнить все поля",
                        "redirect_url": "api/profile",  # Клиент сам решит, как использовать этот URL
                        "message_url": "Вернуться к созданию поста",
                        "requires_auth": True
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    template_name='profile.html'
                )
            else:
                serializer = PictureSerializer(data={
                    "title": request.data['title'],
                    "author": user_profile.id,
                    "image": request.FILES['image'],
                })
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return redirect('/api/profile')
        else:
            return Response(
                {
                    "error": "unauthorized",
                    "message": "Пожалуйста, авторизуйтесь",
                    "redirect_url": "login/",  # Клиент сам решит, как использовать этот URL
                    "message_url": "Перейти к странице входа",
                    "requires_auth": True
                },
                status=status.HTTP_401_UNAUTHORIZED,
                template_name='profile.html'
            )

    @action(methods=['post'], detail=False, url_path='editpicture')
    def editpicture(self, request):
        if request.user.is_authenticated:
            picture = get_object_or_404(Picture, pk=request.data.get('id'), author__user=request.user)
            serializer = PictureSerializer(instance=picture, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return redirect('/api/profile')
        else:
            return Response(
                {
                    "error": "unauthorized",
                    "message": "Пожалуйста, авторизуйтесь",
                    "redirect_url": "login/",  # Клиент сам решит, как использовать этот URL
                    "message_url": "Перейти к странице входа",
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
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Если клиент просит HTML (через заголовок Accept или расширение .html)
        if request.accepted_renderer.format == 'html':
            return Response(
                {
                    'posts': serializer.data
                },
                template_name='home.html'
            )
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='create_comment', renderer_classes=[JSONRenderer])
    def create_comment(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            author_id = user_profile.id
            text = request.data.get('text')
            serializer = CommentSerializer(data={
                "author": author_id,
                "text": text,
                "post": request.data.get('post_id'),
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            text = request.data.get('text')
            serializer = CommentSerializer(data={
                "author": None,
                "text": text,
                "post": request.data.get('post_id'),
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreatePostViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'createpost.html'

    def list(self, request):
        """Отображение HTML страницы с формой"""
        return Response({}, template_name=self.template_name)

    @action(methods=['post'], detail=False, url_path='addpost', renderer_classes=[JSONRenderer])
    def addpost(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            author_id = user_profile.id
            title = request.data.get('title')
            picture_ids = request.data.get('pictures')
            # проблема возникла при создании суперадмина. Для него нет профиля
            # Из-за этого не совпадают id юзеров из модели users и моей модели.
            # Решением является либо удаление полностью базы и создания новой, либо через костыль.
            # пока сделал через костыль
            for picture_id in picture_ids:
                print(Picture.objects.filter(id=picture_id).first().author)
                print(request.user)
                print(picture_id)
                print(request.user.id -1)
                print(Picture.objects.filter(id=picture_id).first().author.id)
                if request.user.id - 1 != Picture.objects.filter(id=picture_id).first().author.id:
                    return Response(
                        {
                            "error": "Bad request",
                            "message": "Ошибка в передаваемых данных",
                            "redirect_url": "login/",
                            "requires_auth": True
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = PostSerializer(data={
                'title': title,
                'author': author_id,
                'picture_ids': picture_ids,
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
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(methods=['get'], detail=False, url_path='getpictures',renderer_classes=[JSONRenderer])
    def getpictures(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            pictures = Picture.objects.filter(author=user_profile)
            serializer = PictureSerializer(pictures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "error": "unauthorized",
                    "message": "Пожалуйста, авторизуйтесь",
                    "redirect_url": "login/",  # Клиент сам решит, как использовать этот URL
                    "requires_auth": True
                },
                status=status.HTTP_401_UNAUTHORIZED
            )