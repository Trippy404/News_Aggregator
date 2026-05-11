import requests
import json

print("=" * 50)
print("Testing RAG Chatbot")
print("=" * 50)

# Test health
print("\n1. Testing health endpoint...")
try:
    response = requests.get("http://localhost:8000/api/chat/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test ask
print("\n2. Asking a question...")
question = "What is the latest news about the stock market?"

try:
    response = requests.post(
        "http://localhost:8000/api/chat/ask",
        json={"question": question},
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📝 Question: {data['question']}")
        print(f"\n🤖 Answer: {data['answer']}")
        print(f"\n📚 Sources ({len(data['sources'])}):")
        for i, source in enumerate(data['sources'], 1):
            print(f"   {i}. {source.get('title', 'No title')[:80]}...")
            print(f"      Source: {source.get('source', 'Unknown')}")
            print(f"      URL: {source.get('source_url', '#')}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("Timeout: The request took too long. The model might still be loading.")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Test complete!")