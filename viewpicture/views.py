from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import RegisterSerializer, LoginSerializer
from django.shortcuts import render
from django.contrib.auth import get_user_model, login

user = get_user_model()

def register_page(request):
    return render(request, 'register.html')
def login_page(request):
    return render(request, 'login.html')

class RegisterView(generics.CreateAPIView):
    queryset = user.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs): #ответ в http
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        temp_user = serializer.save()
        return Response({
            'username': temp_user.username,
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)