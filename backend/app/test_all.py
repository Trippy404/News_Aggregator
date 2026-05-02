# from config import settings

# print("HOST:", settings.MYSQL_HOST)
# print("PORT:", settings.MYSQL_PORT)
# print("USER:", settings.MYSQL_USER)
# print("PASS:", settings.MYSQL_PASSWORD)
# print("DB:", settings.MYSQL_DATABASE)
# print("URL:", settings.DATABASE_URL)
# print("SCRAPING:", settings.SCRAPING_INTERVAL)
# print("CORS:", settings.CORS_ORIGINS)


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime

# from models.news import Base, NewsArticle
# from config import settings

# # 1. Create engine
# engine = create_engine(settings.DATABASE_URL, echo=True)

# # 2. Create tables
# Base.metadata.create_all(engine)

# print("✅ Table created")

# # 3. Create session
# Session = sessionmaker(bind=engine)
# db = Session()

# # 4. Insert test data
# article = NewsArticle(
#     title="Test News",
#     summary="This is a test summary",
#     source="Test Source",
#     source_url="https://example.com/test1",
#     category="Tech",
#     published_at=datetime.now()
# )

# db.add(article)
# db.commit()

# print("✅ Data inserted")

# # 5. Query data
# result = db.query(NewsArticle).all()

# for r in result:
#     print(f"👉 {r.title} | {r.source}")



# from database import SessionLocal, init_db
# from models import User

# # Step 1: Create tables
# init_db()

# # Step 2: Create session
# db = SessionLocal()

# # Step 3: Insert data
# new_user = User(name="Suman")
# db.add(new_user)
# db.commit()

# # Step 4: Query data
# users = db.query(User).all()

# print(users)

# db.close()


# import asyncio
# from scraper.news_scraper import NewsScraper   # adjust path if needed

# async def main():
#     scraper = NewsScraper()
    
#     articles = await scraper.scrape_zerodha_pulse()
    
#     print(f"\nTotal Articles: {len(articles)}\n")
    
#     for i, article in enumerate(articles[:5], 1):
#         print(f"{i}. {article['title']}")
#         print(f"   Source: {article['source']}")
#         print(f"   Category: {article['category']}")
#         print(f"   URL: {article['source_url']}")
#         print("-" * 50)

# if __name__ == "__main__":
#     asyncio.run(main())