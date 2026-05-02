from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from ...database.connection import get_db
from ...models.news import NewsArticle
from ...services.news_service import NewsService

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/")
async def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    category: Optional[str] = None,
    source: Optional[str] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get news articles with filters"""
    query = db.query(NewsArticle)
    
    if category and category != 'all':
        query = query.filter(NewsArticle.category == category)
    if source:
        query = query.filter(NewsArticle.source == source)
    if sentiment:
        query = query.filter(NewsArticle.sentiment_label == sentiment)
    
    total = query.count()
    articles = query.order_by(desc(NewsArticle.published_at)).offset(skip).limit(limit).all()
    
    # Parse keywords and entities
    result = []
    for article in articles:
        article_dict = {
            'id': article.id,
            'title': article.title,
            'summary': article.summary,
            'source': article.source,
            'source_url': article.source_url,
            'category': article.category,
            'published_at': article.published_at.isoformat() if article.published_at else None,
            'sentiment_score': article.sentiment_score,
            'sentiment_label': article.sentiment_label,
            'keywords': article.keywords.split(',') if article.keywords else [],
            'entities': eval(article.entities) if article.entities else {},
            'reading_time': article.reading_time,
            'view_count': article.view_count,
            'share_count': article.share_count
        }
        result.append(article_dict)
    
    return {
        'total': total,
        'skip': skip,
        'limit': limit,
        'articles': result
    }

@router.get("/trending")
async def get_trending_news(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending news based on views"""
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    
    articles = db.query(NewsArticle).filter(
        NewsArticle.published_at >= cutoff_time
    ).order_by(
        desc(NewsArticle.view_count + NewsArticle.share_count * 2)
    ).limit(limit).all()
    
    return [
        {
            'id': a.id,
            'title': a.title,
            'summary': a.summary,
            'source': a.source,
            'view_count': a.view_count,
            'share_count': a.share_count
        }
        for a in articles
    ]

@router.get("/{news_id}")
async def get_news_detail(
    news_id: int,
    db: Session = Depends(get_db)
):
    """Get single news article"""
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News not found")
    
    # Increment view count
    article.view_count += 1
    db.commit()
    db.refresh(article)
    
    return {
        'id': article.id,
        'title': article.title,
        'summary': article.summary,
        'source': article.source,
        'source_url': article.source_url,
        'category': article.category,
        'published_at': article.published_at.isoformat() if article.published_at else None,
        'sentiment_score': article.sentiment_score,
        'sentiment_label': article.sentiment_label,
        'keywords': article.keywords.split(',') if article.keywords else [],
        'entities': eval(article.entities) if article.entities else {},
        'reading_time': article.reading_time,
        'view_count': article.view_count
    }

@router.post("/{news_id}/share")
async def share_article(
    news_id: int,
    db: Session = Depends(get_db)
):
    """Track article share"""
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if article:
        article.share_count += 1
        db.commit()
        return {"message": "Share tracked successfully"}
    raise HTTPException(status_code=404, detail="News not found")

@router.get("/filters/info")
async def get_filter_info(db: Session = Depends(get_db)):
    """Get available filter options"""
    categories = db.query(NewsArticle.category, func.count(NewsArticle.id)).group_by(NewsArticle.category).all()
    sources = db.query(NewsArticle.source, func.count(NewsArticle.id)).group_by(NewsArticle.source).all()
    sentiments = db.query(NewsArticle.sentiment_label, func.count(NewsArticle.id)).group_by(NewsArticle.sentiment_label).all()
    
    return {
        'categories': [{'name': c[0] or 'general', 'count': c[1]} for c in categories],
        'sources': [{'name': s[0], 'count': s[1]} for s in sources],
        'sentiments': [{'name': s[0] or 'neutral', 'count': s[1]} for s in sentiments]
    }