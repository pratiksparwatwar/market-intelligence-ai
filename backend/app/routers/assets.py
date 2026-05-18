from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Article, MarketTheme
from app.schemas import ArticleOut, MarketThemeOut

router = APIRouter(prefix="/api/assets", tags=["assets"])

ASSET_CATEGORIES = [
    "Indian equity market",
    "Gold",
    "Real estate",
    "Crude oil",
    "USD/INR",
    "Bitcoin",
    "Global markets",
]


@router.get("")
def get_assets(db: Session = Depends(get_db)):
    result = []
    for asset in ASSET_CATEGORIES:
        article_count = db.query(Article).filter(
            Article.asset_tags.contains([asset])
        ).count()
        themes = db.query(MarketTheme).filter(
            MarketTheme.affected_assets.contains([asset])
        ).order_by(MarketTheme.generated_at.desc()).limit(1).all()

        result.append({
            "asset": asset,
            "theme_count": db.query(MarketTheme).filter(
                MarketTheme.affected_assets.contains([asset])
            ).count(),
            "article_count": article_count,
            "latest_sentiment": themes[0].sentiment if themes else None,
        })
    return result


@router.get("/{asset}/themes", response_model=List[MarketThemeOut])
def get_asset_themes(asset: str, db: Session = Depends(get_db)):
    return (
        db.query(MarketTheme)
        .filter(MarketTheme.affected_assets.contains([asset]))
        .order_by(MarketTheme.generated_at.desc())
        .limit(20)
        .all()
    )


@router.get("/{asset}/articles", response_model=List[ArticleOut])
def get_asset_articles(asset: str, db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .filter(Article.asset_tags.contains([asset]))
        .order_by(Article.created_at.desc())
        .limit(30)
        .all()
    )
