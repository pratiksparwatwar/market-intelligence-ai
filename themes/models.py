from django.db import models
from news.models import Article


class MarketTheme(models.Model):
    SENTIMENT_CHOICES = [
        ('bullish', 'Bullish'),
        ('bearish', 'Bearish'),
        ('neutral', 'Neutral'),
        ('mixed', 'Mixed'),
    ]
    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    theme_title = models.CharField(max_length=200)
    short_summary = models.TextField()
    why_it_matters = models.TextField()
    affected_assets = models.JSONField(default=list)
    affected_sectors = models.JSONField(default=list)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='neutral')
    confidence_score = models.FloatField(default=0.5)
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='medium')
    supporting_articles = models.ManyToManyField(Article, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at', '-confidence_score']

    def __str__(self):
        return self.theme_title

    @property
    def confidence_pct(self):
        return int(self.confidence_score * 100)
