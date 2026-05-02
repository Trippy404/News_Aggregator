"""
Simple NLP analyzer using only NLTK and TextBlob
No spacy or heavy dependencies required
"""
import nltk
from textblob import TextBlob
from collections import Counter
import re
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist

class SimpleNLPAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    async def extract_keywords(self, text: str, top_k: int = 10) -> list:
        """Extract keywords using frequency analysis"""
        # Clean text
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        
        # Tokenize
        words = word_tokenize(text)
        
        # Remove stopwords and short words
        filtered_words = [w for w in words if w not in self.stop_words and len(w) > 3]
        
        # Get frequency distribution
        freq_dist = FreqDist(filtered_words)
        
        # Return top keywords
        keywords = [word for word, count in freq_dist.most_common(top_k)]
        
        # Also look for capitalized words (proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        for cap in capitalized[:3]:
            if cap.lower() not in keywords and len(cap) > 3:
                keywords.append(cap)
        
        return keywords[:top_k]
    
    async def extract_entities(self, text: str) -> dict:
        """Extract simple named entities using pattern matching"""
        entities = {
            'organizations': [],
            'persons': [],
            'locations': [],
            'dates': [],
            'money': [],
            'products': []
        }
        
        # Pattern for money
        money_pattern = r'\$\d+(?:,\d+)*(?:\.\d+)?|\d+\s+(?:dollars|USD|rupees|Rs\.?)|\d+(?:\.\d+)?\s*(?:million|billion|crore|lakh)'
        money_matches = re.findall(money_pattern, text, re.IGNORECASE)
        entities['money'].extend(money_matches[:5])
        
        # Pattern for dates
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}'
        date_matches = re.findall(date_pattern, text, re.IGNORECASE)
        entities['dates'].extend(date_matches[:5])
        
        # Look for company names
        company_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Ltd|Limited|Inc|Corp|Corporation|LLC)\b'
        company_matches = re.findall(company_pattern, text)
        entities['organizations'].extend(company_matches[:5])
        
        # Look for person names
        person_pattern = r'(?:Mr|Ms|Mrs|Dr)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?'
        person_matches = re.findall(person_pattern, text, re.IGNORECASE)
        entities['persons'].extend(person_matches[:5])
        
        return entities
    
    async def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine label
        if polarity > 0.1:
            label = 'positive'
            score = polarity
        elif polarity < -0.1:
            label = 'negative'
            score = abs(polarity)
        else:
            label = 'neutral'
            score = 0.5
        
        # Word-based sentiment for financial news
        positive_words = ['surge', 'rally', 'gain', 'up', 'growth', 'profit', 'rise', 'high', 'boost', 'positive']
        negative_words = ['fall', 'drop', 'down', 'loss', 'decline', 'crash', 'low', 'slump', 'negative', 'crisis']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        aspect_scores = {
            'bullish': min(pos_count / len(positive_words), 1.0),
            'bearish': min(neg_count / len(negative_words), 1.0),
            'neutral': 1.0 - (max(pos_count, neg_count) / max(len(positive_words), len(negative_words)))
        }
        
        return {
            'label': label,
            'score': score,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'aspect_scores': aspect_scores,
            'compound_score': (polarity + 1) / 2
        }
    
    async def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate extractive summary using sentence scoring"""
        if len(text) <= max_length:
            return text
        
        # Split into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 2:
            return ' '.join(sentences)[:max_length]
        
        # Calculate word frequencies
        words = word_tokenize(text.lower())
        word_freq = {}
        for word in words:
            if word not in self.stop_words and len(word) > 2 and word.isalpha():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = {}
        for sent in sentences:
            sent_words = word_tokenize(sent.lower())
            score = sum(word_freq.get(word, 0) for word in sent_words if word not in self.stop_words)
            if len(sent_words) > 0:
                sentence_scores[sent] = score / len(sent_words)
        
        # Get top 3 sentences
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_sentences = [sent for sent, _ in sorted_sentences[:3]]
        
        # Preserve original order
        summary = ' '.join([sent for sent in sentences if sent in summary_sentences])
        
        return summary[:max_length]
    
    async def calculate_reading_time(self, text: str) -> int:
        """Calculate reading time in minutes (200 words per minute)"""
        words = len(text.split())
        return max(1, words // 200)