from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('register', RegisterView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register', RegisterView.as_view()),
    path('api/', include('viewsexplorer.urls')),
]
