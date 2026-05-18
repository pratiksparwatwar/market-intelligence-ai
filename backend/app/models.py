from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    source = Column(String(100), nullable=False)
    url = Column(String(1000), nullable=False)
    published_at = Column(DateTime, nullable=True)
    raw_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    asset_tags = Column(JSON, default=list)
    sector_tags = Column(JSON, default=list)
    macro_tags = Column(JSON, default=list)
    content_hash = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class MarketTheme(Base):
    __tablename__ = "market_themes"

    id = Column(Integer, primary_key=True, index=True)
    theme_title = Column(String(300), nullable=False)
    short_summary = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    affected_assets = Column(JSON, default=list)
    affected_sectors = Column(JSON, default=list)
    sentiment = Column(String(20), nullable=False)  # bullish/bearish/neutral/mixed
    confidence_score = Column(Float, nullable=False)
    risk_level = Column(String(10), nullable=False)  # low/medium/high
    supporting_article_ids = Column(JSON, default=list)
    generated_at = Column(DateTime, server_default=func.now())
