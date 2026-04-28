from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import *

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('picture', PictureViewSet, basename='picture')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')


router.register('profile',UserProfileViewSet, basename='profile')
router.register('home', PostsViewSet, basename='home')
router.register('createpost', CreatePostViewSet, basename='createpost')



urlpatterns = [
    path('', include(router.urls),),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)