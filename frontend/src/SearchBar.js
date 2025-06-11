import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

function SearchBar({ initialTerm = '', autoFocus = false }) {
    const [query, setQuery] = useState(initialTerm);
    const [isFocused, setIsFocused] = useState(false);
    const inputRef = useRef(null);
    const navigate = useNavigate();

    const handleInput = (e) => setQuery(e.target.value);

    const clearInput = () => {
        setQuery('');
        inputRef.current.focus();
    };

    const handleSend = (e) => {
        if (e) e.preventDefault();
        if (query.trim()) {
            navigate(`/search?term=${encodeURIComponent(query)}`);
        }
    };

    return (
        <form
            className={`search-form${isFocused ? ' focused' : ''}`}
            onSubmit={handleSend}
            style={{ margin: 0 }}
        >
      <span className="search-icon">
        <svg width="20" height="20" fill="none" stroke="gray" strokeWidth="2" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </span>
            <div className="input-wrapper">
                <input
                    ref={inputRef}
                    type="text"
                    className="search-input"
                    placeholder="Enter search term..."
                    value={query}
                    onChange={handleInput}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    autoFocus={autoFocus}
                />
                {query && (
                    <button
                        type="button"
                        className="clear-button"
                        onClick={clearInput}
                        aria-label="Eingabe löschen"
                    >
                        <svg width="18" height="18" fill="none" stroke="gray" strokeWidth="2" viewBox="0 0 24 24">
                            <line x1="18" y1="6" x2="6" y2="18" />
                            <line x1="6" y1="6" x2="18" y2="18" />
                        </svg>
                    </button>
                )}
            </div>
            {query && (
                <button
                    type="button"
                    className="send-button"
                    onClick={handleSend}
                    aria-label="Absenden"
                >
                    <svg width="22" height="22" fill="none" stroke="gray" strokeWidth="2" viewBox="0 0 24 24">
                        <line x1="5" y1="12" x2="19" y2="12" />
                        <polyline points="12 5 19 12 12 19" />
                    </svg>
                </button>
            )}
        </form>
    );
}

export default SearchBar;
