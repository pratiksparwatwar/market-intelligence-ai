import json
from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Article, MarketTheme
from app.prompts.theme_prompt import THEME_GENERATION_SYSTEM, build_theme_prompt

client = AsyncOpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
)


async def generate_themes(db: Session) -> int:
    articles = (
        db.query(Article)
        .order_by(Article.created_at.desc())
        .limit(50)
        .all()
    )

    if len(articles) < 3:
        return 0

    article_dicts = [
        {
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "summary": a.summary or "",
        }
        for a in articles
    ]

    prompt = build_theme_prompt(article_dicts)

    response = await client.chat.completions.create(
        model=settings.DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": THEME_GENERATION_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4000,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    themes_data = data.get("themes", [])

    created = 0
    for t in themes_data:
        theme = MarketTheme(
            theme_title=t.get("theme_title", "Untitled Theme"),
            short_summary=t.get("short_summary", ""),
            why_it_matters=t.get("why_it_matters", ""),
            affected_assets=t.get("affected_assets", []),
            affected_sectors=t.get("affected_sectors", []),
            sentiment=t.get("sentiment", "neutral"),
            confidence_score=float(t.get("confidence_score", 50)),
            risk_level=t.get("risk_level", "medium"),
            supporting_article_ids=t.get("supporting_article_ids", []),
        )
        db.add(theme)
        created += 1

    db.commit()
    return created
