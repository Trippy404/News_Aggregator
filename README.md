# 📰 News Aggregator

A full-stack, AI-powered news aggregation platform that scrapes, stores, and serves news articles through a modern web interface — complete with a RAG (Retrieval-Augmented Generation) chatbot powered by a local LLM.

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python (FastAPI) |
| **Frontend** | JavaScript, CSS, HTML |
| **Database** | MySQL 8.0 |
| **Cache** | Redis 7 |
| **Vector DB** | ChromaDB |
| **Local LLM** | Ollama |
| **Task Queue** | Celery + Celery Beat |
| **Containerization** | Docker & Docker Compose |

---

## ✨ Features

- **Automated News Scraping** — Articles are scraped on a configurable interval (default: every 5 minutes) via background Celery workers.
- **RESTful API** — FastAPI backend serving news data with JWT-based authentication.
- **RAG Chatbot** — Ask questions about the latest news using a locally-running LLM (Ollama) with ChromaDB as the vector store.
- **Redis Caching** — Used for rate limiting and RAG query caching.
- **Scheduled Tasks** — Celery Beat handles periodic scraping and indexing.
- **Fully Dockerized** — One command brings the entire stack up.

---

## 📁 Project Structure

```
News_Aggregator/
├── backend/            # FastAPI application (Python)
├── frontend/           # Web UI (JavaScript / CSS / HTML)
├── mysql-init/         # SQL scripts run on first DB startup
├── scripts/            # Utility/helper scripts
├── .env                # Local environment variables
├── .env.docker         # Docker-specific environment variables
├── docker-compose.yaml # Full service orchestration
├── start.sh            # Linux/macOS startup script
└── start.ps1           # Windows startup script
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Trippy404/News_Aggregator.git
cd News_Aggregator
```

### 2. Configure Environment Variables

Copy the example `.env` file and update values as needed:

```bash
cp .env .env.local
```

Key variables to review:

```env
# Database
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=news_aggregator
MYSQL_USER=news_user
MYSQL_PASSWORD=your_secure_password

# Ports
MYSQL_PORT=3306
REDIS_PORT=6379
CHROMA_PORT=8001
OLLAMA_PORT=11434
BACKEND_PORT=8000
FRONTEND_PORT=80

# Backend
SCRAPING_INTERVAL=300         # in seconds
LOG_LEVEL=info

# Auth
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **Important:** Never commit real credentials to version control. Change all default passwords before deploying.

### 3. Start the Application

**Windows (PowerShell):**
```powershell
./start.ps1
```

**Or directly with Docker Compose:**
```bash
docker compose up --build
```

### 4. Access the App

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| ChromaDB | http://localhost:8001 |
| Ollama | http://localhost:11434 |

---

## 🐳 Docker Services

The `docker-compose.yaml` defines the following services:

| Service | Description |
|---|---|
| `mysql` | MySQL 8.0 relational database |
| `redis` | Redis cache for rate limiting & RAG |
| `chromadb` | Vector database for semantic search |
| `ollama` | Local LLM server for the RAG chatbot |
| `backend` | FastAPI app serving the REST API |
| `celery` | Background worker for scraping tasks |
| `celery-beat` | Scheduler for periodic tasks |
| `frontend` | Nginx-served web UI |

All services communicate over a shared `news_network` bridge network.

---

## 🔧 Development

To run only specific services (e.g. for local backend development):

```bash
docker compose up mysql redis chromadb ollama
```

Then run the backend manually:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## 🛑 Stopping the Application

```bash
docker compose down
```

To also remove all volumes (⚠️ this deletes all stored data):

```bash
docker compose down -v
```

---

## 📦 Persistent Volumes

| Volume | Purpose |
|---|---|
| `news_mysql_data` | MySQL database files |
| `news_redis_data` | Redis AOF persistence |
| `news_chroma_data` | ChromaDB vector embeddings |
| `news_ollama_data` | Ollama model weights |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---
