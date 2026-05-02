from app.database.connection import SessionLocal
from app.models.news import NewsArticle
from datetime import datetime, timedelta
import random

db = SessionLocal()
current = db.query(NewsArticle).count()
needed = 550 - current

print(f"Current articles: {current}")
print(f"Need to add: {needed}")

if needed > 0:
    companies = ['Reliance', 'Tata', 'Infosys', 'HDFC', 'ICICI', 'Wipro', 'Adani', 'Bharti', 'SBI', 'HCL', 'Bajaj', 'Maruti']
    categories = ['markets', 'economy', 'corporate', 'technology', 'international']
    sources = ['Economic Times', 'Moneycontrol', 'Business Standard']
    sentiments = ['positive', 'negative', 'neutral']
    
    for i in range(needed):
        company = random.choice(companies)
        action = random.choice(['announces', 'reports', 'launches', 'considers'])
        subject = random.choice(['profits', 'product', 'expansion', 'acquisition'])
        num = random.randint(1, 999)
        title = f"{company} {action} {subject} {num}"
        
        article = NewsArticle(
            title=title,
            summary=f"Full story: {title}",
            source=random.choice(sources),
            source_url=f"https://news.com/{i}",
            category=random.choice(categories),
            published_at=datetime.now() - timedelta(days=random.randint(0,30)),
            sentiment_score=random.uniform(0.3, 0.9),
            sentiment_label=random.choice(sentiments),
            keywords="news,update",
            entities="{}",
            reading_time=3,
            view_count=random.randint(100, 50000),
            share_count=random.randint(10, 5000)
        )
        db.add(article)
        
        if (i + 1) % 50 == 0:
            db.commit()
            print(f"Added {i+1}/{needed} articles")
    
    db.commit()
    print(f"\n✅ Done! Total articles: {db.query(NewsArticle).count()}")
else:
    print("You already have 500+ articles!")

db.close()