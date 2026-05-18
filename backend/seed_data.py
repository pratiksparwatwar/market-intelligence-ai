"""
Run this to seed sample data for testing:
  python seed_data.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal, Base, engine
from app.models import Article, MarketTheme
from datetime import datetime

Base.metadata.create_all(bind=engine)
db = SessionLocal()

articles = [
    Article(
        title="RBI holds repo rate at 6.5%, signals cautious stance amid global uncertainty",
        source="Economic Times Markets",
        url="https://economictimes.indiatimes.com/sample1",
        published_at=datetime.utcnow(),
        summary="The Reserve Bank of India kept its benchmark repo rate unchanged at 6.5% as expected, maintaining its withdrawal of accommodation stance while monitoring global developments including US Fed policy.",
        asset_tags=["Indian equity market", "USD/INR"],
        sector_tags=["Banking"],
        macro_tags=["monetary policy"],
        content_hash="seed_hash_001",
    ),
    Article(
        title="Gold surges to all-time high as dollar weakens on US inflation data",
        source="Moneycontrol",
        url="https://moneycontrol.com/sample2",
        published_at=datetime.utcnow(),
        summary="Gold prices surged to a new all-time high above $2,400 per ounce as softer-than-expected US inflation data weakened the dollar and boosted safe-haven demand.",
        asset_tags=["Gold", "Global markets"],
        sector_tags=["Metals"],
        macro_tags=["global economy", "monetary policy"],
        content_hash="seed_hash_002",
    ),
    Article(
        title="Sensex rallies 600 points; IT stocks lead gains after strong Q4 results",
        source="Livemint Markets",
        url="https://livemint.com/sample3",
        published_at=datetime.utcnow(),
        summary="The BSE Sensex rose over 600 points as IT majors including TCS and Infosys reported strong Q4 earnings, beating analyst estimates on revenue growth and margin improvement.",
        asset_tags=["Indian equity market"],
        sector_tags=["IT"],
        macro_tags=["India markets"],
        content_hash="seed_hash_003",
    ),
    Article(
        title="Crude oil dips below $80 as OPEC+ signals potential output increase",
        source="Yahoo Finance",
        url="https://finance.yahoo.com/sample4",
        published_at=datetime.utcnow(),
        summary="Crude oil prices fell below the $80 per barrel mark after reports emerged that OPEC+ is considering easing production cuts from Q3 2024 amid adequate global supply levels.",
        asset_tags=["Crude oil", "Global markets"],
        sector_tags=["Energy"],
        macro_tags=["geopolitics", "global economy"],
        content_hash="seed_hash_004",
    ),
    Article(
        title="Bitcoin crosses $70,000 as spot ETF inflows hit record $1.1 billion in a day",
        source="Moneycontrol",
        url="https://moneycontrol.com/sample5",
        published_at=datetime.utcnow(),
        summary="Bitcoin crossed the $70,000 mark for the first time in months, driven by record daily inflows into spot Bitcoin ETFs. Institutional adoption continues to accelerate.",
        asset_tags=["Bitcoin", "Global markets"],
        sector_tags=[],
        macro_tags=["global economy"],
        content_hash="seed_hash_005",
    ),
]

for a in articles:
    existing = db.query(Article).filter(Article.content_hash == a.content_hash).first()
    if not existing:
        db.add(a)

db.commit()

db.refresh(articles[0])
db.refresh(articles[1])
db.refresh(articles[2])

themes = [
    MarketTheme(
        theme_title="RBI Monetary Policy Hold — Banking Sector Watchlist",
        short_summary="The Reserve Bank of India maintained its repo rate at 6.5%, signaling caution amid global uncertainties. This marks the fourth consecutive pause in the rate cycle.",
        why_it_matters="A prolonged rate hold signals that credit costs remain stable for borrowers, providing a neutral-to-slightly-positive backdrop for banking sector margins. Any future rate cut could act as a positive catalyst for rate-sensitive sectors.",
        affected_assets=["Indian equity market", "USD/INR"],
        affected_sectors=["Banking"],
        sentiment="neutral",
        confidence_score=82,
        risk_level="low",
        supporting_article_ids=[articles[0].id],
    ),
    MarketTheme(
        theme_title="Gold Safe-Haven Surge — Dollar Weakness Narrative",
        short_summary="Gold prices broke to new all-time highs driven by US inflation softening and dollar weakness. Safe-haven demand is intensifying amid global macro uncertainty.",
        why_it_matters="Rising gold prices reflect a broader risk-off narrative where investors are rotating into safe assets. This could indicate growing concerns about global growth and currency stability, with possible positive impact on Indian gold-linked assets.",
        affected_assets=["Gold", "USD/INR", "Global markets"],
        affected_sectors=["Metals"],
        sentiment="bullish",
        confidence_score=90,
        risk_level="medium",
        supporting_article_ids=[articles[1].id],
    ),
    MarketTheme(
        theme_title="IT Sector Earnings Beat — Positive Market Intelligence Signal",
        short_summary="Major IT companies reported strong Q4 results, with both revenue growth and margin improvement exceeding analyst expectations, driving a broad equity market rally.",
        why_it_matters="Strong IT earnings signal resilience in the technology export sector despite global headwinds. This could provide a positive sentiment boost to the broader Indian equity market and attract foreign portfolio investors back to IT-heavy indices.",
        affected_assets=["Indian equity market"],
        affected_sectors=["IT"],
        sentiment="bullish",
        confidence_score=85,
        risk_level="low",
        supporting_article_ids=[articles[2].id],
    ),
]

for t in themes:
    db.add(t)

db.commit()
print(f"Seeded {len(articles)} articles and {len(themes)} themes.")
db.close()
