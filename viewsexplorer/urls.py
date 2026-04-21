from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('picture', PictureViewSet, basename='picture')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('test', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls),),
]