from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('', RedirectView.as_view(url='/api/home')),
    path('api/register/', RegisterView.as_view(), name='register_api'),
    path('api/login/', LoginView.as_view(), name='login_api'),
    path('api/', include('viewsexplorer.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)