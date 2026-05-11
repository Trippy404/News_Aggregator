from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading
import time
from .config import settings
from .database.connection import init_db
from .api.routes import news_router, search_router
from .services.news_service import NewsService
from .database.connection import SessionLocal
import asyncio
from app.api.routes.chat import router as chat_router

# Global flag for scraper
scraper_running = False



def run_scraper_periodically():
    """Run scraper in background thread"""
    global scraper_running
    while True:
        if not scraper_running:
            scraper_running = True
            try:
                db = SessionLocal()
                service = NewsService(db)
                asyncio.run(service.scrape_and_process_news())
                db.close()
            except Exception as e:
                print(f"Scraper error: {e}")
            finally:
                scraper_running = False
        time.sleep(settings.SCRAPING_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting application...")
    init_db()
    
    # Start scraper thread
    scraper_thread = threading.Thread(target=run_scraper_periodically, daemon=True)
    scraper_thread.start()
    print("Scraper thread started")
    
    yield
    
    # Shutdown
    print("Shutting down application...")

app = FastAPI(
    title="News Aggregator API",
    description="Advanced news aggregation with NLP",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(news_router)
app.include_router(search_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {
        "message": "News Aggregator API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "news": "/api/news",
            "search": "/api/search",
            "chat": "/api/chat/ask"
        }
    }

@app.get("/health")
async def health_check():
    from .database.connection import SessionLocal
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "MySQL connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}