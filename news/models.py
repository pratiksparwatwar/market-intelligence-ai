from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=100)
    url = models.URLField(max_length=1000, unique=True)
    published_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    asset_tags = models.JSONField(default=list)
    sector_tags = models.JSONField(default=list)
    macro_tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
