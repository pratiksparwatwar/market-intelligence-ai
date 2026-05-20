from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from news.models import Article
from .models import MarketTheme
from .services import generate_themes
from news.services import fetch_and_store_articles


def ping(request):
    return JsonResponse({'status': 'ok'})


def dashboard(request):
    themes = MarketTheme.objects.prefetch_related('supporting_articles').all()[:6]
    recent_articles = Article.objects.order_by('-created_at')[:8]

    asset_watch = {}
    for theme in MarketTheme.objects.all():
        for asset in theme.affected_assets:
            if asset not in asset_watch:
                asset_watch[asset] = {'theme_count': 0, 'sentiments': []}
            asset_watch[asset]['theme_count'] += 1
            asset_watch[asset]['sentiments'].append(theme.sentiment)

    return render(request, 'themes/dashboard.html', {
        'themes': themes,
        'recent_articles': recent_articles,
        'asset_watch': asset_watch,
        'total_articles': Article.objects.count(),
        'total_themes': MarketTheme.objects.count(),
    })


def theme_list(request):
    themes = MarketTheme.objects.all()
    sentiment = request.GET.get('sentiment')
    risk = request.GET.get('risk')
    if sentiment:
        themes = themes.filter(sentiment=sentiment)
    if risk:
        themes = themes.filter(risk_level=risk)
    return render(request, 'themes/list.html', {
        'themes': themes,
        'sentiment_filter': sentiment,
        'risk_filter': risk,
    })


def theme_detail(request, pk):
    theme = get_object_or_404(MarketTheme, pk=pk)
    return render(request, 'themes/detail.html', {'theme': theme})


def admin_panel(request):
    return render(request, 'themes/admin_panel.html', {
        'article_count': Article.objects.count(),
        'theme_count': MarketTheme.objects.count(),
    })


@require_POST
def trigger_fetch_news(request):
    try:
        count = fetch_and_store_articles()
        return JsonResponse({'status': 'success', 'count': count,
                             'message': f'Fetched {count} new articles'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def trigger_generate_themes(request):
    try:
        count = generate_themes()
        return JsonResponse({'status': 'success', 'count': count,
                             'message': f'Generated {count} themes'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def trigger_clear_data(request):
    MarketTheme.objects.all().delete()
    Article.objects.all().delete()
    return JsonResponse({'status': 'success', 'message': 'All data cleared'})


@require_POST
def trigger_refresh_all(request):
    try:
        article_count = fetch_and_store_articles()
        theme_count = generate_themes()
        return JsonResponse({
            'status': 'success',
            'articles_fetched': article_count,
            'themes_generated': theme_count,
            'message': f'Fetched {article_count} articles, generated {theme_count} themes',
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
