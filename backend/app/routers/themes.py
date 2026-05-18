from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import MarketTheme, Article
from app.schemas import MarketThemeOut, MarketThemeDetail

router = APIRouter(prefix="/api/themes", tags=["themes"])


@router.get("", response_model=List[MarketThemeOut])
def get_themes(
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    sentiment: str = None,
    risk_level: str = None,
    db: Session = Depends(get_db),
):
    q = db.query(MarketTheme)
    if sentiment:
        q = q.filter(MarketTheme.sentiment == sentiment)
    if risk_level:
        q = q.filter(MarketTheme.risk_level == risk_level)
    return q.order_by(MarketTheme.generated_at.desc()).offset(skip).limit(limit).all()


@router.get("/{theme_id}", response_model=MarketThemeDetail)
def get_theme(theme_id: int, db: Session = Depends(get_db)):
    theme = db.query(MarketTheme).filter(MarketTheme.id == theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    articles = []
    if theme.supporting_article_ids:
        articles = db.query(Article).filter(Article.id.in_(theme.supporting_article_ids)).all()

    result = MarketThemeDetail.model_validate(theme)
    result.supporting_articles = articles
    return result
