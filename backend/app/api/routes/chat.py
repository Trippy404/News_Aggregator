from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from ...database.connection import get_db
from ...models.news import NewsArticle
from ...services.simple_rag_service import SimpleRAGService
import traceback

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]]
    timestamp: str

@router.post("/ask")
async def ask_question(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Ask a question about current news"""
    try:
        # Validate question
        if not request.question or len(request.question.strip()) < 1:
            raise HTTPException(
                status_code=400, 
                detail="Question must be at least 1 character long"
            )
        
        print(f"📝 Received question: {request.question}")
        
        # Create simple RAG service with database session
        rag_service = SimpleRAGService(db)
        
        # Get answer from RAG service
        result = await rag_service.chat(request.question)
        
        print(f"✅ Generated answer with {len(result.get('sources', []))} sources")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in ask_question: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def chat_health(db: Session = Depends(get_db)):
    """Check if the chat service is healthy"""
    try:
        rag_service = SimpleRAGService(db)
        return {
            'status': 'healthy',
            'type': 'simple_rag',
            'message': 'Using database search (fast mode)'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

@router.get("/stats")
async def get_chat_stats(db: Session = Depends(get_db)):
    """Get statistics about the chatbot"""
    try:
        rag_service = SimpleRAGService(db)
        return rag_service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))