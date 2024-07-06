from django.contrib import admin
from .models import Post 


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'text', 'date_published', 'is_published']
    list_filter = ['date_published']
