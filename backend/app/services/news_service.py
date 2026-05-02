# backend/app/services/news_service.py
from sqlalchemy.orm import Session
from ..models.news import NewsArticle
from ..scraper.news_scraper import NewsScraper
from ..nlp.simple_analyzer import SimpleNLPAnalyzer
from datetime import datetime
import asyncio
import json

class NewsService:
    def __init__(self, db: Session):
        self.db = db
        self.scraper = NewsScraper()
        self.nlp = SimpleNLPAnalyzer()
    
    async def scrape_and_process_news(self):
        """Scrape news from all sources and process with NLP"""
        print("=" * 50)
        print("Starting comprehensive news scraping...")
        print("=" * 50)
        
        # Get articles from all sources
        articles = await self.scraper.scrape_all_sources()
        
        print(f"Total articles fetched: {len(articles)}")
        
        new_count = 0
        for article_data in articles:
            # Check if article already exists
            existing = self.db.query(NewsArticle).filter(
                NewsArticle.title == article_data['title']
            ).first()
            
            if existing:
                continue
            
            # Process with NLP
            full_text = f"{article_data['title']}. {article_data.get('summary', '')}"
            
            keywords = await self.nlp.extract_keywords(full_text)
            entities = await self.nlp.extract_entities(full_text)
            sentiment = article_data.get('sentiment_label') 
            if not sentiment:
                sentiment = await self.nlp.analyze_sentiment(full_text)
            
            reading_time = await self.nlp.calculate_reading_time(full_text)
            
            # Create article
            article = NewsArticle(
                title=article_data['title'],
                summary=article_data.get('summary', article_data['title'][:200]),
                source=article_data.get('source', 'News Source'),
                source_url=article_data.get('source_url', f"https://example.com/news/{datetime.now().timestamp()}"),
                category=article_data.get('category', 'general'),
                published_at=article_data.get('published_at', datetime.now()),
                keywords=','.join(keywords[:10]),
                entities=json.dumps(entities),
                sentiment_score=article_data.get('sentiment_score', sentiment.get('compound_score', 0.5)),
                sentiment_label=article_data.get('sentiment_label', sentiment.get('label', 'neutral')),
                reading_time=reading_time,
                view_count=article_data.get('view_count', 0),
                share_count=article_data.get('share_count', 0)
            )
            
            self.db.add(article)
            new_count += 1
        
        self.db.commit()
        print(f"✓ Added {new_count} new articles to database")
        print(f"Total articles in database: {self.db.query(NewsArticle).count()}")
        print("=" * 50)