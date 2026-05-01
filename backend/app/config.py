from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

class Settings(BaseSettings):
    # MySQL Configuration

    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "news_aggregator")
    
    @property
    def DATABASE_URL(self) -> str:
        password = quote_plus(self.MYSQL_PASSWORD)
        return f"mysql+pymysql://{self.MYSQL_USER}:{password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"

    # Scraping Settings
    SCRAPING_INTERVAL: int = int(os.getenv("SCRAPING_INTERVAL", "300"))
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # class Config:
    #     env_file = ".env"
    #     case_sensitive = True

settings = Settings()