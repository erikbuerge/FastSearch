import React, { useEffect, useState } from 'react';
import SearchBar from './SearchBar';
import './App.css';
import { Link, useSearchParams } from 'react-router-dom';
import CrawlerPopup from "./CrawlerPopup";

function SearchPage() {
    const [result, setResult] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [searchParams] = useSearchParams();
    const term = searchParams.get('term') || '';

    useEffect(() => {
        if (!term) return;
        setLoading(true);
        setError('');
        fetch(`http://127.0.0.1:5000/api/search/${encodeURIComponent(term)}`)
            .then(res => res.json())
            .then(data => {
                if (
                    typeof data === 'string' &&
                    (data === "Search therm not found" || data === "No URLs for the search term")
                ) {
                    setError(data);
                    setResult({});
                } else {
                    setResult(typeof data === 'object' && data !== null ? data : {});
                }
            })
            .catch(() => setError('Fehler bei der Anfrage.'))
            .finally(() => setLoading(false));
    }, [term]);

    return (
        <div className="searchpage-root">
            <CrawlerPopup />
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
                {loading && <p>Loading...</p>}
                {!loading && error && <p style={{ color: 'red' }}>{error}</p>}
                {!loading && !error && Object.keys(result).length === 0 && <p>Keine Ergebnisse gefunden.</p>}
                <ul className="results-list">
                    {Object.entries(result)
                        .filter(([url]) => typeof url === 'string' && url.trim() !== '')
                        .map(([url, title], idx) => (
                            <li key={idx} className="result-item">
                                <a href={url} target="_blank" rel="noopener noreferrer" className="result-link">
                                    <span className="result-title">{title || url.replace(/^https?:\/\//, '')}</span>
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
