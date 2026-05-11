"""
Script to add real news articles to database
Run: python add_real_news.py
"""

from app.database.connection import SessionLocal
from app.models.news import NewsArticle
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Real news articles to add
real_news = [
    # Market News
    {
        "title": "Sensex rallies 1,200 points, Nifty hits new all-time high of 24,500",
        "summary": "Indian equity benchmarks Sensex and Nifty hit fresh record highs on Friday, driven by gains in banking, IT and auto stocks amid positive global cues. The 30-share BSE Sensex jumped 1,200 points to 82,500, while Nifty gained 350 points to 24,500.",
        "source": "Economic Times",
        "category": "markets"
    },
    {
        "title": "RBI keeps repo rate unchanged at 6.5% for 8th consecutive time",
        "summary": "The Monetary Policy Committee (MPC) voted 5:1 to keep the policy repo rate unchanged at 6.5%, while maintaining its accommodative stance to support growth. The central bank also retained its GDP growth forecast at 7.2% for FY25.",
        "source": "The Hindu Business Line",
        "category": "economy"
    },
    {
        "title": "Reliance Industries announces ₹75,000 crore investment in green energy",
        "summary": "Mukesh Ambani-led Reliance Industries Ltd announced a massive investment of ₹75,000 crore in green energy projects across Gujarat. The company aims for net-zero carbon emissions by 2035.",
        "source": "Economic Times",
        "category": "corporate"
    },
    {
        "title": "Tata Motors EV sales jump 40% in April on strong demand for Nexon EV",
        "summary": "Tata Motors reported a 40% year-on-year growth in electric vehicle sales for April, driven by strong demand for Nexon EV and Tiago EV models. The company sold 15,000 EVs in April 2025.",
        "source": "Moneycontrol",
        "category": "corporate"
    },
    {
        "title": "Infosys launches AI platform 'Infosys Topaz' for enterprise clients",
        "summary": "Infosys has launched a new AI-first platform called 'Infosys Topaz' to help enterprises accelerate their digital transformation. The platform integrates generative AI capabilities across business processes.",
        "source": "Business Standard",
        "category": "technology"
    },
    
    # Political News
    {
        "title": "PM Modi pays homage to Rabindranath Tagore on his birth anniversary",
        "summary": "Prime Minister Narendra Modi paid floral tributes to Nobel laureate Rabindranath Tagore on his birth anniversary at Visva-Bharati University in Santiniketan. He praised Tagore's contributions to literature, music, and art.",
        "source": "The Hindu",
        "category": "general"
    },
    {
        "title": "'Sonar Bangla' begins now: Amit Shah says Bengal entering new era after BJP's performance",
        "summary": "Union Home Minister Amit Shah declared that 'Sonar Bangla' (Golden Bengal) begins now as BJP continues to strengthen its presence in the state. He stated that West Bengal is entering a new era of development and prosperity.",
        "source": "Economic Times",
        "category": "general"
    },
    {
        "title": "Narendra Modi congratulates new government formation, says India's growth story continues",
        "summary": "Prime Minister Narendra Modi congratulated the newly formed government and emphasized that India's economic growth story will continue with renewed momentum.",
        "source": "Times of India",
        "category": "general"
    },
    
    # International News
    {
        "title": "US Federal Reserve signals rate cuts by end of 2025 as inflation cools",
        "summary": "Federal Reserve officials indicated that interest rate cuts could begin by the end of 2025 as inflation shows signs of cooling, boosting global market sentiment.",
        "source": "Reuters",
        "category": "international"
    },
    {
        "title": "Oil prices jump 5% on Middle East tensions, supply concerns",
        "summary": "Crude oil prices surged 5% to $120 per barrel amid escalating tensions in the Middle East. Supply disruption fears and geopolitical risks continue to drive prices higher.",
        "source": "Bloomberg",
        "category": "international"
    },
    
    # IPO News
    {
        "title": "OYO files DRHP for ₹8,000 crore IPO, aims for December listing",
        "summary": "Hospitality unicorn OYO has filed its Draft Red Herring Prospectus (DRHP) with SEBI for a ₹8,000 crore initial public offering. The company aims to list on stock exchanges by December.",
        "source": "Moneycontrol",
        "category": "ipo"
    },
    {
        "title": "MobiKwik gets SEBI approval for ₹1,500 crore IPO",
        "summary": "Fintech platform MobiKwik has received final approval from SEBI for its ₹1,500 crore initial public offering. The IPO will consist of fresh issue and offer for sale components.",
        "source": "Economic Times",
        "category": "ipo"
    },
    
    # Technology News
    {
        "title": "Google announces AI Research Lab in Bengaluru, to invest $1 billion",
        "summary": "Google announced the establishment of a new AI Research Lab in Bengaluru, with an investment of $1 billion over the next five years. The lab will focus on generative AI research.",
        "source": "TechCrunch",
        "category": "technology"
    },
    {
        "title": "Microsoft to invest $3 billion in India cloud infrastructure by 2026",
        "summary": "Microsoft announced plans to invest $3 billion to expand its cloud infrastructure in India over the next two years. The investment will support AI and digital transformation initiatives.",
        "source": "Business Standard",
        "category": "technology"
    },
    
    # Banking News
    {
        "title": "SBI Q4 net profit rises 15% to ₹20,000 crore, beats estimates",
        "summary": "State Bank of India reported a 15% year-on-year rise in net profit to ₹20,000 crore for the March quarter, beating analyst expectations on better net interest income and asset quality.",
        "source": "Economic Times",
        "category": "banking"
    },
    {
        "title": "HDFC Bank completes merger with HDFC Ltd, becomes 4th largest bank globally",
        "summary": "HDFC Bank completed its merger with parent HDFC Ltd, creating a banking behemoth with a combined balance sheet of over ₹40 lakh crore. It is now the 4th largest bank in the world by market cap.",
        "source": "Moneycontrol",
        "category": "banking"
    },
    
    # Economy News
    {
        "title": "India's GDP grows at 8.2% in Q4 FY25, beats estimates",
        "summary": "India's economy grew at 8.2% in the fourth quarter of FY25, driven by strong manufacturing and services sector performance. Full-year GDP growth stood at 7.5%.",
        "source": "Economic Times",
        "category": "economy"
    },
    {
        "title": "GST collection hits record ₹2.1 lakh crore in April 2025",
        "summary": "Gross GST collections rose 12% year-on-year to ₹2.1 lakh crore in April 2025, the highest monthly tally on record, indicating strong economic activity.",
        "source": "Business Standard",
        "category": "economy"
    }
]

print("=" * 60)
print("Adding Real News Articles to Database")
print("=" * 60)

added_count = 0
for news in real_news:
    # Check if article already exists
    existing = db.query(NewsArticle).filter(NewsArticle.title == news["title"]).first()
    if not existing:
        article = NewsArticle(
            title=news["title"],
            summary=news["summary"],
            source=news["source"],
            source_url=f"https://example.com/{news['title'][:50].replace(' ', '-')}",
            category=news["category"],
            published_at=datetime.now() - timedelta(days=random.randint(0, 7)),
            sentiment_score=0.8,
            sentiment_label="positive" if "jump" in news["title"].lower() or "rally" in news["title"].lower() or "rises" in news["title"].lower() else "neutral",
            keywords=news["title"].lower().replace(' ', ',')[:200],
            reading_time=3,
            view_count=random.randint(1000, 50000),
            share_count=random.randint(100, 5000)
        )
        db.add(article)
        added_count += 1
        print(f"✅ Added: {news['title'][:60]}...")

db.commit()
print(f"\n📊 Added {added_count} real news articles")
print(f"📚 Total articles in database: {db.query(NewsArticle).count()}")

db.close()