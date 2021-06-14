from django.contrib import admin

from apps.posts.models import Post, Category


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    """
    Display table post on admin panel
    """
    pass


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    """
    Display table Category on admin panel
    """
    pass
