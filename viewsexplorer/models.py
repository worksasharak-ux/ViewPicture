from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

class Picture(models.Model):
    title = models.CharField(max_length=120)
    category = models.ManyToManyField(Category)
    mark = models.BooleanField(default=False)
    image = models.ImageField(null=False, blank=True, upload_to="pictures/")
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='pictures')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=1200)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    pictures = models.ManyToManyField('Picture', blank=False, related_name='posts')

    @property
    def formatted_created_at(self):
        if self.created_at:
            return self.created_at.strftime("%d.%m.%Y %H:%M")
        return 'Дата не указана'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(null=True, blank=True)
