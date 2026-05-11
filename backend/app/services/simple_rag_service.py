"""
Simple RAG Service - Fast, No Vector DB, Just Database Search
Improved keyword extraction for better search results
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict
import re

class SimpleRAGService:
    def __init__(self, db: Session = None):
        self.db = db
    
    def set_db(self, db: Session):
        self.db = db
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from question"""
        # Remove common words
        stop_words = {
            'what', 'is', 'are', 'the', 'a', 'an', 'and', 'or', 'of', 
            'to', 'for', 'in', 'on', 'at', 'by', 'with', 'about', 
            'tell', 'me', 'latest', 'news', 'give', 'summarize', 'please',
            'hi', 'hello', 'hey', 'greetings', 'do', 'does', 'did'
        }
        
        # Extract words
        words = text.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Extract proper nouns (capitalized words - important for brands)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        keywords.extend([p.lower() for p in proper_nouns])
        
        # Extract words with apostrophes or special characters (like MuscleBlaze)
        special_words = re.findall(r'\b[A-Za-z]+[A-Z][a-z]+\b', text)
        keywords.extend([w.lower() for w in special_words])
        
        # For phrases like "Naruto-themed", extract "Naruto"
        phrase_words = re.findall(r'([A-Za-z]+)-', text)
        keywords.extend([w.lower() for w in phrase_words])
        
        return list(set(keywords))[:7]  # Return unique keywords
    
    async def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for news using keywords"""
        if not self.db:
            return []
        
        from app.models.news import NewsArticle
        from sqlalchemy import or_
        
        keywords = self._extract_keywords(query)
        
        print(f"🔍 Extracted keywords: {keywords}")
        
        if not keywords:
            return []
        
        # Build search conditions - search in title and summary
        conditions = []
        for kw in keywords:
            conditions.append(NewsArticle.title.ilike(f'%{kw}%'))
            conditions.append(NewsArticle.summary.ilike(f'%{kw}%'))
        
        # Search database
        results = self.db.query(NewsArticle).filter(
            or_(*conditions)
        ).all()
        
        # Score and sort results
        scored_results = []
        for result in results:
            score = 0
            title_lower = result.title.lower()
            for kw in keywords:
                if kw in title_lower:
                    score += 3  # Title match is more important
                elif kw in (result.summary or '').lower():
                    score += 1
            
            if score > 0:
                scored_results.append({
                    'id': result.id,
                    'title': result.title,
                    'summary': result.summary[:300] if result.summary else '',
                    'source': result.source,
                    'source_url': result.source_url,
                    'category': result.category,
                    'published_at': str(result.published_at) if result.published_at else '',
                    'score': score
                })
        
        # Sort by score (highest first)
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_results[:limit]
    
    async def chat(self, question: str) -> Dict:
        """Main chat function"""
        
        # Handle greetings
        greetings = ['hi', 'hello', 'hey', 'greetings', 'namaste']
        if question.lower().strip() in greetings:
            return {
                'question': question,
                'answer': """📰 **Hello! I'm your News Assistant** 📰

I can help you find news about:
• 📈 Stock Market Updates
• 🏦 Company Results & Announcements
• 📊 Economy & Policy News
• 💻 Technology & Business
• 🏭 Product Launches & Collaborations

**Try asking:**
• "What's the latest market news?"
• "Tell me about SBI"
• "Any news about Reliance?"
• "Economic updates"
• "Technology sector news"

How can I help you today?""",
                'sources': [],
                'timestamp': datetime.now().isoformat()
            }
        
        # Search for news
        results = await self.search(question)
        
        if not results:
            return {
                'question': question,
                'answer': f"📰 I couldn't find news about '{question}'.\n\n💡 Try asking about:\n• Stock market news\n• Specific companies (SBI, Reliance, Tata)\n• Economy or technology\n• Recent business updates",
                'sources': [],
                'timestamp': datetime.now().isoformat()
            }
        
        # Check if we found an exact match for the query
        exact_match = None
        for result in results:
            if result['score'] >= 6:  # High score indicates good match
                exact_match = result
                break
        
        if exact_match:
            # Format detailed response for exact match
            answer = f"📰 **{exact_match['title']}**\n\n"
            answer += f"📝 **Summary:** {exact_match['summary']}\n\n"
            answer += f"📍 **Source:** {exact_match['source']}\n"
            answer += f"📂 **Category:** {exact_match['category']}\n"
            # if exact_match['source_url'] and exact_match['source_url'] != '#':
            #     answer += f"🔗 **Read more:** {exact_match['source_url']}\n"
            
            return {
                'question': question,
                'answer': answer,
                'sources': [exact_match],
                'timestamp': datetime.now().isoformat()
            }
        
        # Format response for multiple results
        answer = f"📰 **Found {len(results)} related news articles:**\n\n"
        for i, article in enumerate(results[:5], 1):
            answer += f"{i}. **{article['title']}**\n"
            answer += f"   📍 Source: {article['source']}\n"
            answer += f"   📂 Category: {article['category']}\n\n"
        
        answer += "💡 Ask for more details about any of these!"
        
        return {
            'question': question,
            'answer': answer,
            'sources': results,
            'timestamp': datetime.now().isoformat()
        }
    
    async def search_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """Simple search method for compatibility"""
        return await self.search(query, n_results)
    
    def get_stats(self) -> Dict:
        """Get service statistics"""
        if self.db:
            from app.models.news import NewsArticle
            total = self.db.query(NewsArticle).count()
            return {
                'type': 'simple_rag',
                'status': 'active',
                'total_articles': total,
                'indexed': 'database_direct'
            }
        return {
            'type': 'simple_rag',
            'status': 'active',
            'indexed': 'database_direct'
        }