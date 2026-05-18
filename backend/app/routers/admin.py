from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article, MarketTheme
from app.services.news_fetcher import fetch_and_store_articles
from app.services.theme_generator import generate_themes
from app.schemas import AdminResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/fetch-news", response_model=AdminResponse)
async def trigger_fetch_news(db: Session = Depends(get_db)):
    try:
        count = await fetch_and_store_articles(db)
        return AdminResponse(status="success", message="News fetched successfully", count=count)
    except Exception as e:
        return AdminResponse(status="error", message=str(e))


@router.post("/generate-themes", response_model=AdminResponse)
async def trigger_generate_themes(db: Session = Depends(get_db)):
    try:
        count = await generate_themes(db)
        return AdminResponse(status="success", message="Themes generated successfully", count=count)
    except Exception as e:
        return AdminResponse(status="error", message=str(e))


@router.delete("/clear-data", response_model=AdminResponse)
def clear_test_data(db: Session = Depends(get_db)):
    theme_count = db.query(MarketTheme).count()
    article_count = db.query(Article).count()
    db.query(MarketTheme).delete()
    db.query(Article).delete()
    db.commit()
    return AdminResponse(
        status="success",
        message=f"Cleared {theme_count} themes and {article_count} articles",
    )
