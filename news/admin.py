from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_at', 'created_at']
    list_filter = ['source']
    search_fields = ['title', 'summary']
    readonly_fields = ['created_at']
