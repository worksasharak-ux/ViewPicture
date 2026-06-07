# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from viewsexplorer.models import Picture, UserProfile

# Просто настраиваем существующую админку
UserAdmin.list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
UserAdmin.list_filter = ('is_staff', 'is_superuser', 'is_active')
UserAdmin.search_fields = ('username', 'email')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_username')
    list_filter = ('user',)
    search_fields = ('user__username', 'user__email')

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username'

