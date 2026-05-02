from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from ...database.connection import get_db
from ...models.news import NewsArticle

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/")
async def search_news(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Search news articles"""
    search_term = f"%{q}%"
    
    articles = db.query(NewsArticle).filter(
        or_(
            NewsArticle.title.like(search_term),
            NewsArticle.summary.like(search_term),
            NewsArticle.keywords.like(search_term)
        )
    ).order_by(
        desc(NewsArticle.published_at)
    ).offset(skip).limit(limit).all()
    
    total = db.query(NewsArticle).filter(
        or_(
            NewsArticle.title.like(search_term),
            NewsArticle.summary.like(search_term),
            NewsArticle.keywords.like(search_term)
        )
    ).count()
    
    return {
        'query': q,
        'total': total,
        'skip': skip,
        'limit': limit,
        'articles': [
            {
                'id': a.id,
                'title': a.title,
                'summary': a.summary,
                'source': a.source,
                'category': a.category,
                'published_at': a.published_at.isoformat() if a.published_at else None,
                'sentiment_label': a.sentiment_label
            }
            for a in articles
        ]
    }