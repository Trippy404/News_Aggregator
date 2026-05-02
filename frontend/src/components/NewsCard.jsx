import React from 'react';
import './NewsCard.css';

const NewsCard = ({ article, onShare, onClick }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'Recently';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  const getSentimentClass = (label) => {
    switch(label?.toLowerCase()) {
      case 'positive': return 'sentiment-positive';
      case 'negative': return 'sentiment-negative';
      default: return 'sentiment-neutral';
    }
  };

  const getSentimentIcon = (label) => {
    switch(label?.toLowerCase()) {
      case 'positive': return '📈';
      case 'negative': return '📉';
      default: return '➖';
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      markets: '📈',
      economy: '🏦',
      corporate: '🏢',
      ipo: '🚀',
      technology: '💻',
      international: '🌍',
      general: '📰'
    };
    return icons[category?.toLowerCase()] || '📰';
  };

  return (
    <div className="news-card" onClick={() => onClick(article)}>
      <div className="card-badge">
        {article.view_count > 100 && <span className="trending-badge">🔥 Trending</span>}
      </div>
      <div className="card-content">
        <div className="card-header">
          <span className="card-category">
            {getCategoryIcon(article.category)} {article.category || 'General'}
          </span>
          <button 
            className="share-button"
            onClick={(e) => {
              e.stopPropagation();
              onShare(article.id);
            }}
            title="Share"
          >
            📤
          </button>
        </div>
        
        <h3 className="card-title">{article.title}</h3>
        <p className="card-summary">{article.summary || 'No summary available'}</p>
        
        <div className="card-meta">
          <span className="meta-source">📰 {article.source}</span>
          <span className={`meta-sentiment ${getSentimentClass(article.sentiment_label)}`}>
            {getSentimentIcon(article.sentiment_label)} {article.sentiment_label || 'Neutral'}
          </span>
        </div>
        
        {article.keywords && article.keywords.length > 0 && (
          <div className="keywords">
            {article.keywords.slice(0, 5).map((keyword, idx) => (
              <span key={idx} className="keyword">#{keyword}</span>
            ))}
          </div>
        )}
        
        <div className="card-footer">
          <span className="timestamp">🕒 {formatDate(article.published_at)}</span>
          <span className="read-time">⏱️ {article.reading_time || 2} min read</span>
          <span className="views">👁️ {article.view_count || 0}</span>
        </div>
      </div>
    </div>
  );
};

export default NewsCard;