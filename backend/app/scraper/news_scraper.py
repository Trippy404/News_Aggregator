import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta
import re
import asyncio
import random
import json

class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    async def scrape_all_sources(self) -> List[Dict]:
        """Scrape news from all available sources"""
        all_articles = []
        
        # Try multiple sources
        sources = [
            self.scrape_zerodha_pulse,
            self.scrape_economic_times,
            self.scrape_moneycontrol,
            self.scrape_business_standard,
            self.get_comprehensive_mock_data  # Fallback
        ]
        
        for source in sources:
            try:
                articles = await source()
                if articles:
                    all_articles.extend(articles)
                    print(f"✓ Got {len(articles)} articles from {source.__name__}")
            except Exception as e:
                print(f"✗ Error from {source.__name__}: {e}")
            
            # Small delay between requests
            await asyncio.sleep(1)
        
        # Remove duplicates based on title similarity
        unique_articles = self.remove_duplicates(all_articles)
        
        return unique_articles
    
    async def scrape_zerodha_pulse(self) -> List[Dict]:
        """Scrape news from Zerodha Pulse"""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get('https://pulse.zerodha.com', headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                # Find all links that might be news articles
                all_links = soup.find_all('a', href=True)
                
                for link in all_links:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    # Check if it looks like a news article
                    if (len(title) > 30 and 
                        len(title) < 200 and
                        href and 
                        ('/news/' in href or '/article/' in href or '/story/' in href)):
                        
                        # Get full URL
                        if href.startswith('/'):
                            href = f"https://pulse.zerodha.com{href}"
                        
                        # Try to get summary from parent
                        parent = link.parent
                        summary = ""
                        if parent:
                            summary_elem = parent.find('p') or parent.find('div', class_=re.compile('summary|desc'))
                            if summary_elem:
                                summary = summary_elem.get_text(strip=True)[:300]
                        
                        articles.append({
                            'title': title,
                            'source_url': href,
                            'source': 'Zerodha Pulse',
                            'summary': summary or title[:200],
                            'published_at': datetime.now() - timedelta(hours=random.randint(1, 48)),
                            'category': self.categorize_news(title, summary)
                        })
                        
                        if len(articles) >= 20:
                            break
                
                return articles
                
            except Exception as e:
                print(f"Zerodha Pulse error: {e}")
                return []
    
    async def scrape_economic_times(self) -> List[Dict]:
        """Scrape news from Economic Times"""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                urls = [
                    'https://economictimes.indiatimes.com/news/markets',
                    'https://economictimes.indiatimes.com/news/economy',
                    'https://economictimes.indiatimes.com/tech/technology'
                ]
                
                articles = []
                for url in urls:
                    response = await client.get(url, headers=self.headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find article links
                    for link in soup.find_all('a', href=True):
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        if (len(title) > 30 and 
                            len(title) < 200 and
                            '/articleshow/' in href):
                            
                            if href.startswith('/'):
                                href = f"https://economictimes.indiatimes.com{href}"
                            
                            articles.append({
                                'title': title,
                                'source_url': href,
                                'source': 'Economic Times',
                                'summary': title,
                                'published_at': datetime.now() - timedelta(hours=random.randint(1, 48)),
                                'category': self.categorize_news(title, '')
                            })
                            
                            if len(articles) >= 15:
                                break
                    
                    await asyncio.sleep(1)
                
                return articles[:20]
                
            except Exception as e:
                print(f"Economic Times error: {e}")
                return []
    
    async def scrape_moneycontrol(self) -> List[Dict]:
        """Scrape news from Moneycontrol"""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get('https://www.moneycontrol.com/news/', headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                for link in soup.find_all('a', href=True):
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if (len(title) > 30 and 
                        len(title) < 200 and
                        '/news/' in href):
                        
                        articles.append({
                            'title': title,
                            'source_url': href if href.startswith('http') else f"https://www.moneycontrol.com{href}",
                            'source': 'Moneycontrol',
                            'summary': title,
                            'published_at': datetime.now() - timedelta(hours=random.randint(1, 48)),
                            'category': self.categorize_news(title, '')
                        })
                        
                        if len(articles) >= 15:
                            break
                
                return articles
                
            except Exception as e:
                print(f"Moneycontrol error: {e}")
                return []
    
    async def scrape_business_standard(self) -> List[Dict]:
        """Scrape news from Business Standard"""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get('https://www.business-standard.com/latest', headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                for link in soup.find_all('a', href=True):
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if (len(title) > 30 and 
                        len(title) < 200 and
                        '/article/' in href):
                        
                        articles.append({
                            'title': title,
                            'source_url': href if href.startswith('http') else f"https://www.business-standard.com{href}",
                            'source': 'Business Standard',
                            'summary': title,
                            'published_at': datetime.now() - timedelta(hours=random.randint(1, 48)),
                            'category': self.categorize_news(title, '')
                        })
                        
                        if len(articles) >= 15:
                            break
                
                return articles
                
            except Exception as e:
                print(f"Business Standard error: {e}")
                return []
    
    def get_comprehensive_mock_data(self) -> List[Dict]:
        """Return comprehensive mock data with many articles"""
        now = datetime.now()
        articles = []
        
        # Financial/Markets news
        markets_news = [
            ("Sensex rallies 1,200 points, Nifty hits new all-time high of 22,800", "markets"),
            ("Bank Nifty surges 3% on strong Q4 results from HDFC Bank, ICICI", "markets"),
            ("IT stocks rebound after 3-day losing streak; Infosys up 4%", "markets"),
            ("FIIs turn net buyers after 5 months, invest ₹12,000 crore in April", "markets"),
            ("Midcap index outperforms benchmarks, gains 8% in April", "markets"),
            ("Volatility index VIX drops 15% as market sentiment improves", "markets"),
            ("PSU banks rally as government announces capital infusion plan", "markets"),
            ("Auto stocks drive higher on strong April sales numbers", "markets"),
            ("Metal stocks shine on global demand recovery, JSW Steel up 6%", "markets"),
            ("Realty stocks surge as housing sales hit 8-year high", "markets"),
        ]
        
        # Economy news
        economy_news = [
            ("India's GDP grows at 8.2% in Q4, beats estimates", "economy"),
            ("RBI keeps repo rate unchanged at 6.5%, cuts CRR by 25 bps", "economy"),
            ("Inflation cools to 4.5% in April on softening food prices", "economy"),
            ("Government to increase CAPEX by 25% to ₹12 lakh crore", "economy"),
            ("IMF raises India's growth forecast to 7.5% for FY25", "economy"),
            ("Current account deficit narrows to 1.2% of GDP", "economy"),
            ("Foreign exchange reserves hit new high of $650 billion", "economy"),
            ("Industrial production grows 6.5% in February", "economy"),
            ("Services PMI rises to 62.5 in April, fastest growth in 14 years", "economy"),
            ("GST collection hits record ₹2.1 lakh crore in April", "economy"),
        ]
        
        # Corporate news
        corporate_news = [
            ("Reliance Industries Q4 profit jumps 15% to ₹25,000 crore", "corporate"),
            ("Tata Motors announces ₹5,000 crore share buyback", "corporate"),
            ("HDFC Bank completes merger with HDFC, becomes 4th largest bank globally", "corporate"),
            ("Infosys launches AI platform 'Infosys Topaz 2.0'", "corporate"),
            ("Adani Group plans ₹50,000 crore investment in data centers", "corporate"),
            ("Wipro acquires AI startup for $500 million", "corporate"),
            ("ICICI Bank reports record quarterly profit of ₹12,000 crore", "corporate"),
            ("Maruti Suzuki hikes prices by 2% on rising input costs", "corporate"),
            ("Bharti Airtel launches 5G services in 500 cities", "corporate"),
            ("Zomato turns profitable for first time, shares jump 15%", "corporate"),
        ]
        
        # Technology news
        tech_news = [
            ("Google announces AI Research Lab in Bengaluru", "technology"),
            ("Microsoft to invest $3 billion in India cloud infrastructure", "technology"),
            ("Paytm reports strong growth in UPI transactions", "technology"),
            ("Ola Electric launches new electric scooter starting at ₹80,000", "technology"),
            ("PhonePe crosses 500 million users milestone", "technology"),
            ("CRED acquires expense management startup", "technology"),
            ("BYJU's raises $500 million at $22 billion valuation", "technology"),
            ("Swiggy announces IPO plans, aims to raise ₹10,000 crore", "technology"),
            ("Zerodha launches new trading platform with AI features", "technology"),
            ("Unacademy cuts losses by 50% in FY24", "technology"),
        ]
        
        # International news
        intl_news = [
            ("US Fed signals rate cuts in September, markets rally", "international"),
            ("Oil prices jump 5% on Middle East tensions", "international"),
            ("China's economy grows 5.2% in Q1, beats expectations", "international"),
            ("European Central Bank cuts rates for first time in 5 years", "international"),
            ("Japan intervenes to support yen at 160 level", "international"),
            ("Bitcoin hits new all-time high of $85,000", "international"),
            ("Elon Musk announces new Tesla factory in India", "international"),
            ("Apple to manufacture iPhone 17 in India starting 2025", "international"),
            ("Nvidia surpasses Apple as world's second most valuable company", "international"),
            ("Amazon invests $10 billion in India cloud infrastructure", "international"),
        ]
        
        # IPO news
        ipo_news = [
            ("OYO files DRHP for ₹8,000 crore IPO", "ipo"),
            ("MobiKwik gets SEBI approval for ₹1,500 crore IPO", "ipo"),
            ("Pharmeasy postpones IPO citing market conditions", "ipo"),
            ("Lenskart plans ₹5,000 crore IPO in 2025", "ipo"),
            ("Boat's parent company files for ₹2,000 crore IPO", "ipo"),
        ]
        
        # Combine all news
        all_news = markets_news + economy_news + corporate_news + tech_news + intl_news + ipo_news
        
        for i, (title, category) in enumerate(all_news):
            # Create realistic timestamps over the last 7 days
            hours_ago = i * 3  # Spread news over time
            published_time = now - timedelta(hours=hours_ago)
            
            # Generate view counts
            views = random.randint(100, 50000)
            
            # Generate sentiment based on title
            sentiment = self.get_sentiment_from_title(title)
            
            articles.append({
                'title': title,
                'source_url': f"https://example.com/news/{i}",
                'source': random.choice(['Economic Times', 'The Hindu Business Line', 'Moneycontrol', 'Business Standard', 'Zerodha Pulse']),
                'summary': f"Full story: {title}. Read more for detailed analysis and expert opinions on this development.",
                'published_at': published_time,
                'category': category,
                'view_count': views,
                'share_count': views // 10,
                'sentiment_label': sentiment['label'],
                'sentiment_score': sentiment['score']
            })
        
        return articles
    
    def get_sentiment_from_title(self, title: str) -> dict:
        """Determine sentiment from title keywords"""
        positive_words = ['surge', 'rally', 'gain', 'up', 'growth', 'profit', 'rise', 'high', 'boost', 'positive', 'record', 'jump']
        negative_words = ['fall', 'drop', 'down', 'loss', 'decline', 'crash', 'low', 'slump', 'negative', 'crisis', 'cut']
        
        title_lower = title.lower()
        pos_count = sum(1 for word in positive_words if word in title_lower)
        neg_count = sum(1 for word in negative_words if word in title_lower)
        
        if pos_count > neg_count:
            return {'label': 'positive', 'score': 0.8}
        elif neg_count > pos_count:
            return {'label': 'negative', 'score': 0.7}
        else:
            return {'label': 'neutral', 'score': 0.5}
    
    def categorize_news(self, title: str, summary: str) -> str:
        """Categorize news using keywords"""
        text = f"{title} {summary}".lower()
        
        categories = {
            'markets': ['stock', 'nifty', 'sensex', 'market', 'bse', 'nse', 'trading', 'index', 'shares', 'rally', 'benchmark', 'volatility'],
            'economy': ['gdp', 'economy', 'fiscal', 'budget', 'rbi', 'policy', 'inflation', 'growth', 'economic', 'repo', 'rate', 'gst', 'fiscal'],
            'corporate': ['company', 'corporate', 'earnings', 'profit', 'revenue', 'acquisition', 'ceo', 'rel', 'tata', 'infosys', 'hdfc', 'bank', 'corp'],
            'ipo': ['ipo', 'listing', 'public issue', 'subscription', 'draft', 'red herring'],
            'technology': ['ai', 'tech', 'digital', 'startup', 'software', 'app', 'platform', 'google', 'microsoft', 'apple', 'amazon', 'meta'],
            'international': ['us', 'global', 'world', 'fed', 'japan', 'china', 'europe', 'international', 'oil', 'bitcoin', 'crypto']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'
    
    def remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            # Simple title-based deduplication
            title_key = article['title'].lower()[:100]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        return unique_articles