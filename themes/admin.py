from django.contrib import admin
from .models import MarketTheme


@admin.register(MarketTheme)
class MarketThemeAdmin(admin.ModelAdmin):
    list_display = ['theme_title', 'sentiment', 'risk_level', 'confidence_score', 'generated_at']
    list_filter = ['sentiment', 'risk_level']
    filter_horizontal = ['supporting_articles']
    readonly_fields = ['generated_at']
