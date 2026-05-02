import spacy
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from typing import List, Dict, Tuple
import nltk
import json
import re

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

class LightweightNLPAnalyzer:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
    
    async def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract keywords from text"""
        doc = self.nlp(text)
        keywords = set()
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON", "GPE", "MONEY", "PRODUCT"]:
                keywords.add(ent.text)
        
        # Extract important nouns and proper nouns
        for token in doc:
            if (token.pos_ in ["NOUN", "PROPN"] and 
                token.text.lower() not in self.stop_words and 
                len(token.text) > 3):
                keywords.add(token.text)
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3 and len(chunk.text) > 3:
                keywords.add(chunk.text)
        
        return list(keywords)[:top_k]
    
    async def extract_entities(self, text: str) -> Dict:
        """Extract named entities"""
        doc = self.nlp(text)
        entities = {
            'organizations': [],
            'persons': [],
            'locations': [],
            'dates': [],
            'money': [],
            'products': []
        }
        
        entity_map = {
            'ORG': 'organizations',
            'PERSON': 'persons',
            'GPE': 'locations',
            'LOC': 'locations',
            'DATE': 'dates',
            'MONEY': 'money',
            'PRODUCT': 'products'
        }
        
        for ent in doc.ents:
            if ent.label_ in entity_map:
                entities[entity_map[ent.label_]].append(ent.text)
        
        # Deduplicate and limit
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))[:10]
        
        return entities
    
    async def analyze_sentiment(self, text: str) -> Dict:
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
        
        # Aspect-based sentiment for financial news
        aspect_scores = {
            'bullish': self._check_aspect(text, ['surge', 'rally', 'gain', 'up', 'growth', 'profit', 'rise']),
            'bearish': self._check_aspect(text, ['fall', 'drop', 'down', 'loss', 'decline', 'crash', 'fall']),
            'neutral': self._check_aspect(text, ['stable', 'steady', 'unchanged', 'flat'])
        }
        
        return {
            'label': label,
            'score': score,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'aspect_scores': aspect_scores,
            'compound_score': (polarity + 1) / 2
        }
    
    def _check_aspect(self, text: str, keywords: List[str]) -> float:
        """Check aspect presence in text"""
        text_lower = text.lower()
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        return min(matches / len(keywords), 1.0)
    
    async def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate extractive summary"""
        if len(text) <= max_length:
            return text
        
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 2:
            return ' '.join(sentences)[:max_length]
        
        # Calculate word frequencies
        words = word_tokenize(text.lower())
        word_freq = FreqDist(w for w in words if w not in self.stop_words and w.isalnum())
        
        # Score sentences
        sentence_scores = {}
        for sent in sentences:
            sent_words = word_tokenize(sent.lower())
            score = sum(word_freq.get(word, 0) for word in sent_words if word not in self.stop_words)
            if len(sent_words) > 0:
                sentence_scores[sent] = score / len(sent_words)
        
        # Get top sentences
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_sentences = [sent for sent, _ in sorted_sentences[:3]]
        
        # Preserve original order
        summary = ' '.join([sent for sent in sentences if sent in summary_sentences])
        
        return summary[:max_length]
    
    async def calculate_reading_time(self, text: str) -> int:
        """Calculate reading time in minutes"""
        words = len(text.split())
        return max(1, words // 200)