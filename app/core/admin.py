from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Admin panel configuration for User model"""

    list_display = ["username", "first_name", "last_name", "is_staff"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_superuser", "is_active")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )


class PostAdmin(admin.ModelAdmin):
    """Admin panel for Post model"""

    list_display = ['title', 'author', 'created_at']
    list_filter = ['author', 'created_at']


class CommentAdmin(admin.ModelAdmin):
    """Admin panel for Comment model"""

    list_display = ['post', 'author', 'created_at']
    list_filter = ['post', 'author']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
