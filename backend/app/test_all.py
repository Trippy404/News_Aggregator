# from config import settings

# print("HOST:", settings.MYSQL_HOST)
# print("PORT:", settings.MYSQL_PORT)
# print("USER:", settings.MYSQL_USER)
# print("PASS:", settings.MYSQL_PASSWORD)
# print("DB:", settings.MYSQL_DATABASE)
# print("URL:", settings.DATABASE_URL)
# print("SCRAPING:", settings.SCRAPING_INTERVAL)
# print("CORS:", settings.CORS_ORIGINS)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models.news import Base, NewsArticle
from config import settings

# 1. Create engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# 2. Create tables
Base.metadata.create_all(engine)

print("✅ Table created")

# 3. Create session
Session = sessionmaker(bind=engine)
db = Session()

# 4. Insert test data
article = NewsArticle(
    title="Test News",
    summary="This is a test summary",
    source="Test Source",
    source_url="https://example.com/test1",
    category="Tech",
    published_at=datetime.now()
)

db.add(article)
db.commit()

print("✅ Data inserted")

# 5. Query data
result = db.query(NewsArticle).all()

for r in result:
    print(f"👉 {r.title} | {r.source}")