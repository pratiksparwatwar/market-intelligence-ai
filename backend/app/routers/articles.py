from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Article
from app.schemas import ArticleOut

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("", response_model=List[ArticleOut])
def get_articles(
    skip: int = 0,
    limit: int = Query(default=50, le=200),
    source: str = None,
    db: Session = Depends(get_db),
):
    q = db.query(Article)
    if source:
        q = q.filter(Article.source == source)
    return q.order_by(Article.created_at.desc()).offset(skip).limit(limit).all()
