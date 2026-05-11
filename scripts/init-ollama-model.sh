#!/bin/bash

echo "========================================="
echo "System Health Monitor"
echo "========================================="
echo ""

# Check Docker services
echo "📦 Docker Services Status:"
echo "------------------------"
docker-compose ps

echo ""
echo "📊 Resource Usage:"
echo "------------------------"
docker stats --no-stream

echo ""
echo "📈 Database Statistics:"
echo "------------------------"
docker exec news_mysql mysql -u news_user -pSecureNewsPass456! -e "
USE news_aggregator;
SELECT COUNT(*) as Total_Articles, 
       COUNT(DISTINCT category) as Categories,
       COUNT(DISTINCT source) as Sources
FROM news_articles;
" 2>/dev/null

echo ""
echo "🔍 ChromaDB Status:"
echo "------------------------"
curl -s http://localhost:8001/api/v1/heartbeat | python -m json.tool 2>/dev/null || echo "ChromaDB not responding"

echo ""
echo "🤖 Ollama Status:"
echo "------------------------"
curl -s http://localhost:11434 | python -m json.tool 2>/dev/null || echo "Ollama not responding"

echo ""
echo "✅ Monitor complete!"