import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.models.news import NewsArticle
from app.services.rag_service import RAGService

async def index_all_news():
    print("=" * 50)
    print("Indexing News Articles for RAG Chatbot")
    print("=" * 50)
    
    db = SessionLocal()
    rag = RAGService()
    
    articles = db.query(NewsArticle).all()
    print(f"Found {len(articles)} articles to index")
    
    article_data = []
    for article in articles:
        article_data.append({
            'id': article.id,
            'title': article.title,
            'summary': article.summary,
            'category': article.category,
            'source': article.source,
            'source_url': article.source_url,
            'keywords': article.keywords,
            'sentiment_label': article.sentiment_label,
            'published_at': article.published_at
        })
    
    await rag.index_articles(article_data)
    
    print(f"✅ Indexing complete!")
    print(f"Total indexed: {rag.collection.count()}")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(index_all_news())