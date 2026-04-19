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
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

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
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ForeignKey('Picture', on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(null=True, blank=True)
