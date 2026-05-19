from django.shortcuts import render
from .models import Article


def articles_list(request):
    source_filter = request.GET.get('source')
    articles = Article.objects.order_by('-created_at')
    if source_filter:
        articles = articles.filter(source=source_filter)
    articles = articles[:100]
    sources = Article.objects.values_list('source', flat=True).distinct().order_by('source')
    return render(request, 'news/articles.html', {
        'articles': articles,
        'sources': sources,
        'source_filter': source_filter,
    })
