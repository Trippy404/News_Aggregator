import React, { useState } from 'react';
import './SmartFilters.css';

const SmartFilters = ({ open, onClose, onApply, filterInfo }) => {
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedSentiment, setSelectedSentiment] = useState('');

  const handleApply = () => {
    onApply({
      categories: selectedCategories,
      sentiment: selectedSentiment
    });
    onClose();
  };

  const handleReset = () => {
    setSelectedCategories([]);
    setSelectedSentiment('');
  };

  if (!open) return null;

  return (
    <>
      <div className="filters-overlay" onClick={onClose}></div>
      <div className="filters-sidebar">
        <div className="filters-header">
          <h3>🔍 Smart Filters</h3>
          <button className="close-filters" onClick={onClose}>✕</button>
        </div>
        
        <div className="filters-content">
          <div className="filter-section">
            <h4>Categories</h4>
            <div className="filter-options">
              {filterInfo?.categories?.filter(c => c.name !== 'general').map(cat => (
                <label key={cat.name} className="filter-option">
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(cat.name)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedCategories([...selectedCategories, cat.name]);
                      } else {
                        setSelectedCategories(selectedCategories.filter(c => c !== cat.name));
                      }
                    }}
                  />
                  <span>{cat.name}</span>
                  <span className="option-count">({cat.count})</span>
                </label>
              ))}
            </div>
          </div>
          
          <div className="filter-section">
            <h4>Sentiment</h4>
            <div className="filter-options">
              {['positive', 'negative', 'neutral'].map(sent => (
                <label key={sent} className="filter-option">
                  <input
                    type="radio"
                    name="sentiment"
                    checked={selectedSentiment === sent}
                    onChange={() => setSelectedSentiment(sent)}
                  />
                  <span>{sent.charAt(0).toUpperCase() + sent.slice(1)}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
        
        <div className="filters-footer">
          <button className="reset-btn" onClick={handleReset}>Reset</button>
          <button className="apply-btn" onClick={handleApply}>Apply Filters</button>
        </div>
      </div>
    </>
  );
};

export default SmartFilters;