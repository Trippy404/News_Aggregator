import React from 'react';
import './FilterBar.css';

const FilterBar = ({ activeCategory, onCategoryChange, onOpenFilters, filterInfo }) => {
  const categories = [
    { id: 'all', name: 'All', icon: '📰' },
    { id: 'trending', name: 'Trending', icon: '🔥' },
    { id: 'markets', name: 'Markets', icon: '📈' },
    { id: 'economy', name: 'Economy', icon: '🏦' },
    { id: 'corporate', name: 'Corporate', icon: '🏢' },
    { id: 'technology', name: 'Technology', icon: '💻' },
    { id: 'international', name: 'International', icon: '🌍' },
  ];

  const getCategoryCount = (categoryId) => {
    if (!filterInfo?.categories || categoryId === 'trending') return 0;
    const cat = filterInfo.categories.find(c => c.name === categoryId);
    return cat ? cat.count : 0;
  };

  return (
    <div className="filter-bar">
      <div className="filter-header">
        <span className="filter-title">📊 News Categories</span>
        <button className="advanced-filter-btn" onClick={onOpenFilters}>
          🔍 Advanced Filters
        </button>
      </div>
      
      <div className="filter-chips">
        {categories.map(cat => (
          <button
            key={cat.id}
            className={`filter-chip ${activeCategory === cat.id ? 'active' : ''}`}
            onClick={() => onCategoryChange(cat.id)}
          >
            <span className="chip-icon">{cat.icon}</span>
            <span className="chip-name">{cat.name}</span>
            {cat.id !== 'trending' && cat.id !== 'all' && (
              <span className="chip-count">{getCategoryCount(cat.id)}</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

export default FilterBar;