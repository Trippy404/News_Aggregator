import React, { useState, useEffect } from 'react';
import './App.css';
import NewsCard from './components/NewsCard';
import FilterBar from './components/FilterBar';
import SearchBar from './components/SeachBar';
import SmartFilters from './components/SmartFilters';
import { fetchNews, searchNews, getTrendingNews, getFilterInfo } from './services/api';

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterInfo, setFilterInfo] = useState(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [totalArticles, setTotalArticles] = useState(0);
  const [loadingMore, setLoadingMore] = useState(false);

  useEffect(() => {
    loadFilterInfo();
  }, []);

  useEffect(() => {
    // Reset when category or search changes
    setPage(0);
    setNews([]);
    setHasMore(true);
    loadNews(true);
  }, [activeCategory, searchQuery]);

  useEffect(() => {
    // Load more when page changes and not first page
    if (page > 0) {
      loadNews(false);
    }
  }, [page]);

  const loadFilterInfo = async () => {
    try {
      const info = await getFilterInfo();
      setFilterInfo(info);
    } catch (err) {
      console.error('Failed to load filter info:', err);
    }
  };

  const loadNews = async (reset = false) => {
    try {
      if (reset) {
        setLoading(true);
      } else {
        setLoadingMore(true);
      }
      
      let data;
      const skip = page * 100;
      
      if (searchQuery) {
        data = await searchNews(searchQuery, { skip, limit: 100 });
        if (reset) {
          setNews(data.articles || []);
        } else {
          setNews(prev => [...prev, ...(data.articles || [])]);
        }
        setTotalArticles(data.total || 0);
        setHasMore(data.articles?.length === 100);
      } else if (activeCategory === 'trending') {
        data = await getTrendingNews(200);
        setNews(data || []);
        setHasMore(false);
        setTotalArticles(data?.length || 0);
      } else {
        const category = activeCategory === 'all' ? null : activeCategory;
        data = await fetchNews({ category, skip, limit: 100 });
        if (reset) {
          setNews(data.articles || []);
        } else {
          setNews(prev => [...prev, ...(data.articles || [])]);
        }
        setTotalArticles(data.total || 0);
        setHasMore(data.has_more || false);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to load news. Please make sure the backend server is running on port 8000');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const handleShare = async (articleId) => {
    try {
      console.log('Shared article:', articleId);
    } catch (err) {
      console.error('Failed to track share:', err);
    }
  };

  const handleNewsClick = (article) => {
    if (article && article.source_url) {
      window.open(article.source_url, '_blank');
    }
  };

  const loadMore = () => {
    if (!loadingMore && hasMore) {
      setPage(prev => prev + 1);
    }
  };

  return (
    <div className="app">
      <nav className="navbar">
        <div className="navbar-container">
          <div className="logo">
            <span className="logo-icon">📰</span>
            <span className="logo-text">NewsAggregator</span>
          </div>
          <ul className="nav-links">
            <li>
              <a 
                href="#" 
                className={activeCategory === 'all' ? 'active' : ''} 
                onClick={(e) => { e.preventDefault(); setActiveCategory('all'); setSearchQuery(''); }}
              >
                All News
              </a>
            </li>
            <li>
              <a 
                href="#" 
                className={activeCategory === 'trending' ? 'active' : ''} 
                onClick={(e) => { e.preventDefault(); setActiveCategory('trending'); setSearchQuery(''); }}
              >
                Trending
              </a>
            </li>
            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setFiltersOpen(true); }}>
                Filters
              </a>
            </li>
          </ul>
          <SearchBar onSearch={setSearchQuery} />
        </div>
      </nav>

      <main className="container">
        <FilterBar 
          activeCategory={activeCategory}
          onCategoryChange={(cat) => { setActiveCategory(cat); setSearchQuery(''); }}
          onOpenFilters={() => setFiltersOpen(true)}
          filterInfo={filterInfo}
        />

        {error && (
          <div className="error-alert">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading news...</p>
          </div>
        ) : (
          <>
            <div className="article-count">
              Showing {news.length} of {totalArticles} articles
            </div>
            
            <div className="news-grid">
              {news.length > 0 ? (
                news.map((article, index) => (
                  <NewsCard
                    key={article.id || index}
                    article={article}
                    onShare={handleShare}
                    onClick={handleNewsClick}
                  />
                ))
              ) : (
                <div className="no-results">
                  <p>No news articles found.</p>
                </div>
              )}
            </div>

            {hasMore && news.length > 0 && (
              <div className="load-more-container">
                <button 
                  className="load-more-btn"
                  onClick={loadMore}
                  disabled={loadingMore}
                >
                  {loadingMore ? 'Loading...' : `Load More Articles (${news.length} / ${totalArticles})`}
                </button>
              </div>
            )}

            {loadingMore && (
              <div className="loading-more">
                <div className="spinner-small"></div>
                <p>Loading more articles...</p>
              </div>
            )}
          </>
        )}
      </main>

      <SmartFilters 
        open={filtersOpen}
        onClose={() => setFiltersOpen(false)}
        onApply={(filters) => {
          console.log('Applied filters:', filters);
          setFiltersOpen(false);
        }}
        filterInfo={filterInfo}
      />
    </div>
  );
}

export default App;