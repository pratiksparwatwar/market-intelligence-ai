from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ArticleOut(BaseModel):
    id: int
    title: str
    source: str
    url: str
    published_at: Optional[datetime]
    summary: Optional[str]
    asset_tags: List[str]
    sector_tags: List[str]
    macro_tags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MarketThemeOut(BaseModel):
    id: int
    theme_title: str
    short_summary: str
    why_it_matters: str
    affected_assets: List[str]
    affected_sectors: List[str]
    sentiment: str
    confidence_score: float
    risk_level: str
    supporting_article_ids: List[int]
    generated_at: datetime

    class Config:
        from_attributes = True


class MarketThemeDetail(MarketThemeOut):
    supporting_articles: List[ArticleOut] = []


class AssetSummary(BaseModel):
    asset: str
    theme_count: int
    article_count: int
    latest_sentiment: Optional[str]


class AdminResponse(BaseModel):
    status: str
    message: str
    count: Optional[int] = None
