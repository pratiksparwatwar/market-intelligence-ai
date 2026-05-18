THEME_GENERATION_SYSTEM = """You are a market intelligence analyst. Your job is to read financial news articles and identify key market themes.

Rules:
- Never say "buy" or "sell"
- Never give direct investment advice
- Use terms like: market intelligence, risk indicator, possible impact, watchlist, sentiment, narrative
- Be objective and factual
- Always base insights on the provided articles only
- Return ONLY valid JSON, no markdown, no extra text"""


def build_theme_prompt(articles: list[dict]) -> str:
    articles_text = "\n\n".join([
        f"[ID:{a['id']}] {a['source'].upper()}: {a['title']}\n{a.get('summary', '')}"
        for a in articles
    ])

    return f"""Analyze these financial news articles and identify 3-7 distinct market themes.

ARTICLES:
{articles_text}

Return ONLY this JSON structure (no markdown, no extra text):
{{
  "themes": [
    {{
      "theme_title": "concise theme name",
      "short_summary": "2-3 sentence summary of what is happening",
      "why_it_matters": "explanation of market significance and possible impact on assets/sectors",
      "affected_assets": ["Indian equity market", "Gold", "USD/INR", etc],
      "affected_sectors": ["Banking", "IT", "Energy", etc],
      "sentiment": "bullish|bearish|neutral|mixed",
      "confidence_score": 0-100,
      "risk_level": "low|medium|high",
      "supporting_article_ids": [list of article IDs from the input]
    }}
  ]
}}

Asset options: Indian equity market, Gold, Real estate, Crude oil, USD/INR, Bitcoin, Global markets
Sentiment: bullish, bearish, neutral, or mixed
Risk level: low, medium, or high
Confidence: 0-100 based on how many articles support this theme"""
