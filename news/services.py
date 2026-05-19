import hashlib
import time
from datetime import datetime

import feedparser
from bs4 import BeautifulSoup
from django.utils import timezone

from .models import Article

RSS_SOURCES = [
    {"name": "Moneycontrol", "url": "https://www.moneycontrol.com/rss/latestnews.xml"},
    {"name": "ET Markets", "url": "https://economictimes.indiatimes.com/markets/rss.cms"},
    {"name": "Livemint", "url": "https://www.livemint.com/rss/markets"},
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/news/rss/"},
    {"name": "RBI", "url": "https://www.rbi.org.in/rss.aspx"},
    {"name": "Investing.com", "url": "https://www.investing.com/rss/news.rss"},
]

ASSET_KEYWORDS = {
    "Nifty 50": ["nifty", "nifty 50", "nifty50"],
    "Sensex": ["sensex", "bse 30"],
    "Gold": ["gold", "mcx gold"],
    "Silver": ["silver"],
    "Crude Oil": ["crude oil", "crude", "brent", "wti"],
    "USD/INR": ["rupee", "usd/inr", "dollar", "forex"],
    "Bitcoin": ["bitcoin", "btc"],
    "Ethereum": ["ethereum", "eth"],
    "Bank Nifty": ["bank nifty", "banknifty"],
    "Midcap": ["midcap", "mid cap", "nifty midcap"],
}

SECTOR_KEYWORDS = {
    "Banking": ["bank", "banking", "rbi", "nbfc", "hdfc", "sbi", "icici", "axis bank"],
    "IT": ["it sector", "infosys", "tcs", "wipro", "tech mahindra", "hcl tech", "software"],
    "Pharma": ["pharma", "pharmaceutical", "drug", "medicine", "healthcare"],
    "Auto": ["auto", "automobile", "car", "ev", "electric vehicle", "maruti", "tata motors"],
    "Energy": ["energy", "power", "oil", "gas", "reliance", "ongc", "ntpc"],
    "FMCG": ["fmcg", "consumer", "hindustan unilever", "itc", "nestle"],
    "Metals": ["metal", "steel", "aluminium", "copper", "tata steel", "jsw"],
    "Real Estate": ["real estate", "realty", "property", "dlf", "housing"],
    "Telecom": ["telecom", "jio", "airtel", "vodafone", "5g"],
    "Infra": ["infrastructure", "infra", "roads", "railways", "airport"],
}

MACRO_KEYWORDS = {
    "Inflation": ["inflation", "cpi", "wpi", "price rise"],
    "Interest Rates": ["interest rate", "repo rate", "monetary policy", "mpc", "rate hike", "rate cut"],
    "GDP": ["gdp", "economic growth", "economy"],
    "FII/DII": ["fii", "dii", "foreign investor", "institutional investor", "fpi"],
    "Budget": ["budget", "fiscal", "government spending", "tax"],
    "Global Markets": ["fed", "federal reserve", "dow jones", "s&p 500", "nasdaq", "global market"],
    "Geopolitics": ["geopolitical", "war", "trade war", "sanctions", "tariff"],
    "IPO": ["ipo", "initial public offering", "listing"],
    "Earnings": ["earnings", "quarterly results", "q1", "q2", "q3", "q4", "revenue", "profit"],
}


def _tag(text, keywords_map):
    text_lower = text.lower()
    return [tag for tag, kws in keywords_map.items() if any(kw in text_lower for kw in kws)]


def fetch_and_store_articles():
    new_count = 0
    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:20]:
                title = entry.get("title", "").strip()
                url = entry.get("link", "").strip()
                if not title or not url:
                    continue

                raw_summary = entry.get("summary", "") or entry.get("description", "")
                summary = BeautifulSoup(raw_summary, "html.parser").get_text()[:500] if raw_summary else ""

                published_at = None
                if getattr(entry, "published_parsed", None):
                    published_at = timezone.make_aware(
                        datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    )

                combined = f"{title} {summary}"

                try:
                    Article.objects.create(
                        title=title,
                        source=source["name"],
                        url=url,
                        published_at=published_at,
                        summary=summary,
                        asset_tags=_tag(combined, ASSET_KEYWORDS),
                        sector_tags=_tag(combined, SECTOR_KEYWORDS),
                        macro_tags=_tag(combined, MACRO_KEYWORDS),
                    )
                    new_count += 1
                except Exception:
                    continue
        except Exception:
            continue
    return new_count
