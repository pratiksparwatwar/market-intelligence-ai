import json

import openai
from django.conf import settings

from news.models import Article
from .models import MarketTheme

SYSTEM_PROMPT = """You are a financial market intelligence analyst for Indian markets.
Your role is to identify key market themes from recent news.

STRICT RULES:
- Never use "buy", "sell", "invest", "purchase", or "recommend" language
- Use terms like: "market intelligence", "risk indicator", "possible impact", "watchlist", "sentiment", "narrative"
- Base all insights only on the provided articles
- Return ONLY valid JSON with no other text or markdown"""


def generate_themes():
    articles = list(Article.objects.order_by('-created_at')[:50])
    if not articles:
        return 0

    articles_text = "\n".join(
        f"{i+1}. [{a.source}] {a.title}"
        + (f" | Assets: {a.asset_tags}" if a.asset_tags else "")
        + (f" | Sectors: {a.sector_tags}" if a.sector_tags else "")
        for i, a in enumerate(articles)
    )

    user_prompt = f"""Analyze these {len(articles)} recent Indian market news articles and identify 3-7 major market themes.

ARTICLES:
{articles_text}

Return a JSON array. Each item must have exactly these fields:
[
  {{
    "theme_title": "concise theme name (max 10 words)",
    "short_summary": "2-3 sentence summary of what is happening",
    "why_it_matters": "what market participants are watching and why",
    "affected_assets": ["list of affected assets or indices"],
    "affected_sectors": ["list of affected sectors"],
    "sentiment": "bullish or bearish or neutral or mixed",
    "confidence_score": 0.0,
    "risk_level": "low or medium or high",
    "article_indices": [1, 2, 3]
  }}
]

Return ONLY the JSON array. No markdown, no explanation."""

    client = openai.OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        timeout=90,
    )

    response = client.chat.completions.create(
        model=settings.DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    themes_data = json.loads(content)

    MarketTheme.objects.all().delete()

    created = 0
    for item in themes_data:
        theme = MarketTheme.objects.create(
            theme_title=item.get("theme_title", ""),
            short_summary=item.get("short_summary", ""),
            why_it_matters=item.get("why_it_matters", ""),
            affected_assets=item.get("affected_assets", []),
            affected_sectors=item.get("affected_sectors", []),
            sentiment=item.get("sentiment", "neutral"),
            confidence_score=float(item.get("confidence_score", 0.5)),
            risk_level=item.get("risk_level", "medium"),
        )
        for idx in item.get("article_indices", []):
            if 1 <= idx <= len(articles):
                theme.supporting_articles.add(articles[idx - 1])
        created += 1

    return created
