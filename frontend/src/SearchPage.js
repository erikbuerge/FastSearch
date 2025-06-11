import React, { useEffect, useState } from 'react';
import SearchBar from './SearchBar';
import './App.css';
import { Link, useSearchParams } from 'react-router-dom';

function SearchPage() {
    const [result, setResult] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchParams] = useSearchParams();
    const term = searchParams.get('term') || '';

    useEffect(() => {
        if (!term) return;
        setLoading(true);
        fetch(`http://127.0.0.1:5000/api/search/${encodeURIComponent(term)}`)
            .then(res => res.json())
            .then(data => setResult(Array.isArray(data) ? data : []))
            .finally(() => setLoading(false));
    }, [term]);

    return (
        <div className="searchpage-root">
            <div className="searchpage-bar-row">
                <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none', color: 'inherit' }}>
                    <img src="/icon.png" alt="Logo" className="search-logo" />
                    <span className="search-title" style={{ fontSize: '2rem', marginLeft: 12 }}>FastSearch</span>
                </Link>
                <div className="searchpage-bar">
                    <SearchBar initialTerm={term} />
                </div>
            </div>
            <div className="searchpage-results">
                <h2>Fast search results for &quot;{term}&quot;</h2>
                {loading && <p>Lade...</p>}
                {!loading && result.length === 0 && <p>Keine Ergebnisse gefunden.</p>}
                <ul className="results-list">
                    {result.map((url, idx) => (
                        <li key={idx} className="result-item">
                            <a href={url} target="_blank" rel="noopener noreferrer" className="result-link">
                                <span className="result-title">{url.replace(/^https?:\/\//, '')}</span>
                                <span className="result-url">{url}</span>
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default SearchPage;
