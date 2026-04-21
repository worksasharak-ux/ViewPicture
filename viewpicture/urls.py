from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('api/register/', RegisterView.as_view(), name='register_api'),
    path('api/login/', LoginView.as_view(), name='login_api'),
    path('api/', include('viewsexplorer.urls')),
]
