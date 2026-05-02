# backend/import_historical_news.py
"""Script to import historical news data"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
import random
import json

sys.path.append(os.path.dirname(__file__))

from app.database.connection import SessionLocal, init_db
from app.models.news import NewsArticle
from app.nlp.simple_analyzer import SimpleNLPAnalyzer

async def import_historical_data():
    """Import historical news data"""
    print("=" * 60)
    print("Importing Historical News Data")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    nlp = SimpleNLPAnalyzer()
    
    # Comprehensive news data
    news_data = [
        # Markets News (20 articles)
        ("Sensex rallies 1,200 points, Nifty hits new all-time high of 22,800", "markets", "Economic Times", "positive"),
        ("Bank Nifty surges 3% on strong Q4 results from HDFC Bank, ICICI", "markets", "Moneycontrol", "positive"),
        ("IT stocks rebound after 3-day losing streak; Infosys up 4%", "markets", "Economic Times", "positive"),
        ("FIIs turn net buyers after 5 months, invest ₹12,000 crore in April", "markets", "Business Standard", "positive"),
        ("Midcap index outperforms benchmarks, gains 8% in April", "markets", "The Hindu Business Line", "positive"),
        ("Volatility index VIX drops 15% as market sentiment improves", "markets", "Moneycontrol", "positive"),
        ("PSU banks rally as government announces capital infusion plan", "markets", "Economic Times", "positive"),
        ("Auto stocks drive higher on strong April sales numbers", "markets", "Business Standard", "positive"),
        ("Metal stocks shine on global demand recovery, JSW Steel up 6%", "markets", "Moneycontrol", "positive"),
        ("Realty stocks surge as housing sales hit 8-year high", "markets", "Economic Times", "positive"),
        ("Markets end lower on profit booking after 5-day rally", "markets", "The Hindu Business Line", "negative"),
        ("RBI's hawkish stance triggers sell-off in banking stocks", "markets", "Moneycontrol", "negative"),
        ("Global uncertainty weighs on markets, Sensex down 800 points", "markets", "Economic Times", "negative"),
        ("FPIs withdraw ₹7,000 crore from Indian equities in April", "markets", "Business Standard", "negative"),
        ("IT sector faces headwinds as US recession fears loom", "markets", "Moneycontrol", "negative"),
        
        # Economy News (15 articles)
        ("India's GDP grows at 8.2% in Q4, beats estimates", "economy", "Economic Times", "positive"),
        ("RBI keeps repo rate unchanged at 6.5%, cuts CRR by 25 bps", "economy", "The Hindu Business Line", "positive"),
        ("Inflation cools to 4.5% in April on softening food prices", "economy", "Moneycontrol", "positive"),
        ("Government to increase CAPEX by 25% to ₹12 lakh crore", "economy", "Business Standard", "positive"),
        ("IMF raises India's growth forecast to 7.5% for FY25", "economy", "Economic Times", "positive"),
        ("Current account deficit narrows to 1.2% of GDP", "economy", "The Hindu Business Line", "positive"),
        ("Foreign exchange reserves hit new high of $650 billion", "economy", "Moneycontrol", "positive"),
        ("Industrial production grows 6.5% in February", "economy", "Business Standard", "positive"),
        ("Services PMI rises to 62.5 in April, fastest growth in 14 years", "economy", "Economic Times", "positive"),
        ("GST collection hits record ₹2.1 lakh crore in April", "economy", "The Hindu Business Line", "positive"),
        
        # Corporate News (20 articles)
        ("Reliance Industries Q4 profit jumps 15% to ₹25,000 crore", "corporate", "Economic Times", "positive"),
        ("Tata Motors announces ₹5,000 crore share buyback", "corporate", "Moneycontrol", "positive"),
        ("HDFC Bank completes merger with HDFC, becomes 4th largest bank globally", "corporate", "Business Standard", "positive"),
        ("Infosys launches AI platform 'Infosys Topaz 2.0'", "corporate", "Economic Times", "positive"),
        ("Adani Group plans ₹50,000 crore investment in data centers", "corporate", "The Hindu Business Line", "positive"),
        ("Wipro acquires AI startup for $500 million", "corporate", "Moneycontrol", "positive"),
        ("ICICI Bank reports record quarterly profit of ₹12,000 crore", "corporate", "Business Standard", "positive"),
        ("Maruti Suzuki hikes prices by 2% on rising input costs", "corporate", "Economic Times", "neutral"),
        ("Bharti Airtel launches 5G services in 500 cities", "corporate", "Moneycontrol", "positive"),
        ("Zomato turns profitable for first time, shares jump 15%", "corporate", "The Hindu Business Line", "positive"),
        ("TCS wins $1 billion deal from UK-based client", "corporate", "Economic Times", "positive"),
        ("HCL Tech announces special dividend of ₹50 per share", "corporate", "Moneycontrol", "positive"),
        ("SBI Card reports 25% growth in spending", "corporate", "Business Standard", "positive"),
        ("Asian Paints expands capacity with new plant in Gujarat", "corporate", "Economic Times", "positive"),
        ("Bajaj Finance crosses ₹1 lakh crore AUM milestone", "corporate", "Moneycontrol", "positive"),
        
        # Technology News (15 articles)
        ("Google announces AI Research Lab in Bengaluru", "technology", "Economic Times", "positive"),
        ("Microsoft to invest $3 billion in India cloud infrastructure", "technology", "Moneycontrol", "positive"),
        ("Paytm reports strong growth in UPI transactions", "technology", "Business Standard", "positive"),
        ("Ola Electric launches new electric scooter starting at ₹80,000", "technology", "The Hindu Business Line", "positive"),
        ("PhonePe crosses 500 million users milestone", "technology", "Economic Times", "positive"),
        ("CRED acquires expense management startup", "technology", "Moneycontrol", "positive"),
        ("BYJU's raises $500 million at $22 billion valuation", "technology", "Business Standard", "positive"),
        ("Swiggy announces IPO plans, aims to raise ₹10,000 crore", "technology", "Economic Times", "positive"),
        ("Zerodha launches new trading platform with AI features", "technology", "Moneycontrol", "positive"),
        ("Unacademy cuts losses by 50% in FY24", "technology", "The Hindu Business Line", "positive"),
        
        # International News (15 articles)
        ("US Fed signals rate cuts in September, markets rally", "international", "Economic Times", "positive"),
        ("Oil prices jump 5% on Middle East tensions", "international", "Moneycontrol", "negative"),
        ("China's economy grows 5.2% in Q1, beats expectations", "international", "Business Standard", "positive"),
        ("European Central Bank cuts rates for first time in 5 years", "international", "Economic Times", "positive"),
        ("Japan intervenes to support yen at 160 level", "international", "The Hindu Business Line", "neutral"),
        ("Bitcoin hits new all-time high of $85,000", "international", "Moneycontrol", "positive"),
        ("Elon Musk announces new Tesla factory in India", "international", "Economic Times", "positive"),
        ("Apple to manufacture iPhone 17 in India starting 2025", "international", "Business Standard", "positive"),
        ("Nvidia surpasses Apple as world's second most valuable company", "international", "Moneycontrol", "positive"),
        ("Amazon invests $10 billion in India cloud infrastructure", "international", "Economic Times", "positive"),
        
        # IPO News (10 articles)
        ("OYO files DRHP for ₹8,000 crore IPO", "ipo", "Economic Times", "positive"),
        ("MobiKwik gets SEBI approval for ₹1,500 crore IPO", "ipo", "Moneycontrol", "positive"),
        ("Pharmeasy postpones IPO citing market conditions", "ipo", "Business Standard", "negative"),
        ("Lenskart plans ₹5,000 crore IPO in 2025", "ipo", "The Hindu Business Line", "positive"),
        ("Boat's parent company files for ₹2,000 crore IPO", "ipo", "Economic Times", "positive"),
    ]
    
    print(f"Preparing to import {len(news_data)} news articles...")
    
    new_count = 0
    for i, (title, category, source, sentiment_label) in enumerate(news_data):
        # Check if article already exists
        existing = db.query(NewsArticle).filter(NewsArticle.title == title).first()
        
        if existing:
            continue
        
        # Generate summary
        summary = f"{title}. Read more for detailed analysis and expert insights on this development."
        
        # Generate realistic timestamps (spread over last 7 days)
        hours_ago = i * 4  # Spread news over time
        published_at = datetime.now() - timedelta(hours=hours_ago)
        
        # Generate view counts
        view_count = random.randint(500, 50000)
        share_count = view_count // 10
        
        # Process with NLP for keywords and entities
        full_text = f"{title}. {summary}"
        keywords = await nlp.extract_keywords(full_text)
        entities = await nlp.extract_entities(full_text)
        reading_time = await nlp.calculate_reading_time(full_text)
        
        # Sentiment score
        sentiment_score = 0.8 if sentiment_label == 'positive' else (0.3 if sentiment_label == 'negative' else 0.5)
        
        # Create article
        article = NewsArticle(
            title=title,
            summary=summary,
            source=source,
            source_url=f"https://example.com/news/article_{i}",
            category=category,
            published_at=published_at,
            keywords=','.join(keywords[:8]),
            entities=json.dumps(entities),
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            reading_time=reading_time,
            view_count=view_count,
            share_count=share_count
        )
        
        db.add(article)
        new_count += 1
        
        if new_count % 20 == 0:
            db.commit()
            print(f"✓ Imported {new_count} articles so far...")
    
    # Final commit
    db.commit()
    
    total_articles = db.query(NewsArticle).count()
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully imported {new_count} new articles!")
    print(f"📊 Total articles in database: {total_articles}")
    print("=" * 60)
    
    # Print category distribution
    from sqlalchemy import func
    categories = db.query(NewsArticle.category, func.count(NewsArticle.id)).group_by(NewsArticle.category).all()
    print("\n📁 Category Distribution:")
    for category, count in categories:
        print(f"   {category}: {count} articles")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(import_historical_data())