from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Index
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"
    __table_args__ = (
        Index('idx_published_source', 'published_at', 'source'),
        Index('idx_category_sentiment', 'category', 'sentiment_score'),
        Index('idx_source_datetime', 'source', 'published_at'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    source = Column(String(100), nullable=False, index=True)
    source_url = Column(String(500), unique=True, nullable=False, index=True)
    category = Column(String(50), index=True)
    published_at = Column(DateTime, nullable=False, index=True)
    scraped_at = Column(DateTime, server_default=func.now())
    
    # NLP fields
    sentiment_score = Column(Float, default=0.0)
    sentiment_label = Column(String(20), index=True)
    keywords = Column(Text)  # Comma-separated keywords
    entities = Column(Text)  # JSON string of entities
    reading_time = Column(Integer, default=3)
    view_count = Column(Integer, default=0, index=True)
    share_count = Column(Integer, default=0)