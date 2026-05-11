"""
Fast Indexing - Optimized for Speed
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.models.news import NewsArticle
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm
import time

def fast_index():
    print("=" * 50)
    print("🚀 FAST INDEXING - Optimized Version")
    print("=" * 50)
    
    start_time = time.time()
    
    # Connect to database
    db = SessionLocal()
    articles = db.query(NewsArticle).all()
    print(f"📚 Found {len(articles)} articles")
    
    if len(articles) == 0:
        print("⚠️ No articles found!")
        db.close()
        return
    
    # Initialize ChromaDB (reuse existing)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection for fresh start
    try:
        chroma_client.delete_collection("news_articles")
    except:
        pass
    
    # Create new collection with optimized embedding function
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    collection = chroma_client.create_collection(
        name="news_articles",
        embedding_function=embedding_fn
    )
    
    # Batch processing for speed
    batch_size = 50
    batch_ids = []
    batch_documents = []
    batch_metadatas = []
    
    print("💾 Indexing articles in batches...")
    
    for i, article in enumerate(tqdm(articles, desc="Indexing")):
        # Skip fake news
        title = article.title.lower()
        if any(word in title for word in ['launches product', 'reports product', 'announces product']):
            continue
        
        # Create document text
        doc_text = f"{article.title} {article.summary[:200] if article.summary else ''}"
        
        batch_ids.append(f"article_{article.id}")
        batch_documents.append(doc_text)
        batch_metadatas.append({
            'title': article.title,
            'source': article.source,
            'category': article.category,
            'source_url': article.source_url,
            'id': article.id
        })
        
        # Insert batch when full
        if len(batch_ids) >= batch_size:
            collection.add(
                ids=batch_ids,
                documents=batch_documents,
                metadatas=batch_metadatas
            )
            batch_ids = []
            batch_documents = []
            batch_metadatas = []
    
    # Insert remaining
    if batch_ids:
        collection.add(
            ids=batch_ids,
            documents=batch_documents,
            metadatas=batch_metadatas
        )
    
    elapsed = time.time() - start_time
    print(f"\n✅ Indexing complete!")
    print(f"📊 Total indexed: {collection.count()}")
    print(f"⏱️ Time taken: {elapsed:.2f} seconds")
    
    db.close()

if __name__ == "__main__":
    fast_index()