import hashlib
import feedparser
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Article

RSS_SOURCES = [
    {
        "name": "Moneycontrol",
        "url": "https://www.moneycontrol.com/rss/latestnews.xml",
        "asset_tags": ["Indian equity market"],
        "sector_tags": [],
        "macro_tags": ["India markets"],
    },
    {
        "name": "Economic Times Markets",
        "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "asset_tags": ["Indian equity market"],
        "sector_tags": [],
        "macro_tags": ["India markets"],
    },
    {
        "name": "Livemint Markets",
        "url": "https://www.livemint.com/rss/markets",
        "asset_tags": ["Indian equity market"],
        "sector_tags": [],
        "macro_tags": ["India markets"],
    },
    {
        "name": "Yahoo Finance",
        "url": "https://finance.yahoo.com/news/rssindex",
        "asset_tags": ["Global markets"],
        "sector_tags": [],
        "macro_tags": ["global economy"],
    },
    {
        "name": "Investing.com",
        "url": "https://www.investing.com/rss/news.rss",
        "asset_tags": ["Global markets"],
        "sector_tags": [],
        "macro_tags": ["global economy"],
    },
    {
        "name": "RBI",
        "url": "https://www.rbi.org.in/scripts/rss.aspx",
        "asset_tags": ["Indian equity market", "USD/INR"],
        "sector_tags": ["Banking"],
        "macro_tags": ["monetary policy", "RBI"],
    },
]

ASSET_KEYWORDS = {
    "Gold": ["gold", "bullion", "mcx gold", "yellow metal"],
    "Crude oil": ["crude", "oil", "petroleum", "brent", "wti", "opec"],
    "Bitcoin": ["bitcoin", "btc", "crypto", "cryptocurrency"],
    "USD/INR": ["rupee", "usd/inr", "dollar", "forex", "currency"],
    "Real estate": ["real estate", "realty", "property", "housing", "reit"],
    "Indian equity market": ["sensex", "nifty", "bse", "nse", "equity", "stocks", "shares"],
    "Global markets": ["dow", "nasdaq", "s&p", "ftse", "global markets", "fed", "fed rate"],
}

SECTOR_KEYWORDS = {
    "Banking": ["bank", "nbfc", "rbi", "credit", "loan", "npa"],
    "IT": ["infosys", "tcs", "wipro", "tech mahindra", "software", "it sector"],
    "Energy": ["energy", "power", "electricity", "solar", "renewable"],
    "Pharma": ["pharma", "drug", "medicine", "healthcare", "fda"],
    "Auto": ["auto", "automobile", "vehicle", "ev", "electric vehicle"],
    "FMCG": ["fmcg", "consumer goods", "hul", "itc"],
    "Metals": ["steel", "metals", "aluminium", "copper", "iron"],
    "Telecom": ["telecom", "jio", "airtel", "5g", "broadband"],
}

MACRO_KEYWORDS = {
    "monetary policy": ["interest rate", "repo rate", "fed", "rbi", "inflation", "cpi", "wpi"],
    "geopolitics": ["war", "sanctions", "geopolit", "trade war", "tariff"],
    "fiscal policy": ["budget", "gst", "tax", "fiscal deficit", "government spending"],
    "global economy": ["recession", "gdp", "imf", "world bank", "global growth"],
}


def _tag_from_text(text: str, keyword_map: dict) -> list[str]:
    text_lower = text.lower()
    return [tag for tag, keywords in keyword_map.items() if any(kw in text_lower for kw in keywords)]


def _make_hash(url: str, title: str) -> str:
    return hashlib.sha256(f"{url}:{title}".encode()).hexdigest()


def _parse_date(entry) -> Optional[datetime]:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6])
            except Exception:
                pass
    return None


def _extract_summary(entry) -> str:
    summary = getattr(entry, "summary", "") or ""
    if summary:
        soup = BeautifulSoup(summary, "html.parser")
        return soup.get_text(separator=" ", strip=True)[:1000]
    return ""


async def fetch_and_store_articles(db: Session) -> int:
    stored = 0
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        for source in RSS_SOURCES:
            try:
                resp = await client.get(source["url"])
                feed = feedparser.parse(resp.text)
            except Exception:
                try:
                    feed = feedparser.parse(source["url"])
                except Exception:
                    continue

            for entry in feed.entries[:20]:
                title = getattr(entry, "title", "").strip()
                url = getattr(entry, "link", "").strip()
                if not title or not url:
                    continue

                content_hash = _make_hash(url, title)
                existing = db.query(Article).filter(Article.content_hash == content_hash).first()
                if existing:
                    continue

                summary = _extract_summary(entry)
                full_text = f"{title} {summary}"

                asset_tags = list(set(source["asset_tags"] + _tag_from_text(full_text, ASSET_KEYWORDS)))
                sector_tags = list(set(source["sector_tags"] + _tag_from_text(full_text, SECTOR_KEYWORDS)))
                macro_tags = list(set(source["macro_tags"] + _tag_from_text(full_text, MACRO_KEYWORDS)))

                article = Article(
                    title=title,
                    source=source["name"],
                    url=url,
                    published_at=_parse_date(entry),
                    summary=summary,
                    raw_text=summary,
                    asset_tags=asset_tags,
                    sector_tags=sector_tags,
                    macro_tags=macro_tags,
                    content_hash=content_hash,
                )
                db.add(article)
                stored += 1

    db.commit()
    return stored
