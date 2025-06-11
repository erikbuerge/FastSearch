import React, { useEffect, useState } from 'react';
import SearchBar from './SearchBar';
import './App.css';
import { Link, useSearchParams } from 'react-router-dom';

function SearchPage() {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [searchParams] = useSearchParams();
    const term = searchParams.get('term') || '';

    useEffect(() => {
        if (!term) return;
        setLoading(true);
        fetch(`http://127.0.0.1:5000/api/search/${encodeURIComponent(term)}`)
            .then(res => res.json())
            .then(data => setResult(data))
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
                <h2>Fast search results for "{term}"</h2>
                {loading && <p>Lade...</p>}
                <pre>{result ? JSON.stringify(result, null, 2) : 'No data'}</pre>
            </div>
        </div>
    );
}

export default SearchPage;
