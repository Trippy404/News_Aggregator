Write-Host " Starting News Aggregator with RAG Chatbot" -ForegroundColor Cyan

# Copy environment file
Copy-Item .env.docker .env -Force

# Build and start containers
Write-Host " Building Docker images..." -ForegroundColor Yellow
docker-compose build

Write-Host " Starting containers..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services
Write-Host " Waiting for services to start (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Initialize database
Write-Host " Initializing database..." -ForegroundColor Green
docker exec news_backend python -c "from app.database.connection import init_db; init_db()"

# Index news for RAG
Write-Host " Indexing news articles..." -ForegroundColor Green
docker exec news_backend python index_news.py

# Pull LLM model
Write-Host " Pulling Mistral model (this may take a few minutes)..." -ForegroundColor Green
docker exec news_ollama ollama pull mistral

Write-Host "`n Setup complete!" -ForegroundColor Green
Write-Host " Frontend: http://localhost" -ForegroundColor Cyan
Write-Host " API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host " Chatbot: Click the chat icon on the frontend" -ForegroundColor Cyan
Write-Host "`nTo stop: docker-compose down" -ForegroundColor Yellow