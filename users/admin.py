from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Допълнителна информация', {'fields': ('is_moderator',)}),
    )
    list_display = ('username', 'email', 'is_moderator', 'is_staff')

admin.site.register(Profile)