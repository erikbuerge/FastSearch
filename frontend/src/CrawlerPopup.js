import React, { useState } from 'react';
import './App.css';
import Spinner from './Spinner';

const CrawlerPopup = () => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [formData, setFormData] = useState({
        startUrl: '',
        depth: '',
        minLength: '',
        maxAmount: ''
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const closePopup = () => {
        setIsPopupOpen(false);
        setMessage('');
    };

    // Polling Funktion
    const pollCrawler = async (url, interval = 1500, maxAttempts = 30) => {
        let attempts = 0;
        while (attempts < maxAttempts) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/crawler/${url}`);
                if (response.ok) {
                    const data = await response.json();
                    setMessage(data.message || 'Crawler started successfully');
                    setTimeout(() => closePopup(), 2000);
                    return;
                }
            } catch (error) {
                // Fehler ignorieren, Polling fortsetzen
            }
            attempts++;
            await new Promise(res => setTimeout(res, interval));
        }
        setMessage('Timeout: Crawler konnte nicht gestartet werden.');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');
        await pollCrawler(formData.startUrl);
        setLoading(false);
    };

    return (
        <div className="crawler-control">
            <button
                className="icon-button"
                onClick={() => setIsPopupOpen(true)}
                aria-label="Open crawler settings"
            >
                🕷️
            </button>

            {isPopupOpen && (
                <div
                    className="popup-overlay"
                    onClick={(e) => {
                        if (e.target === e.currentTarget) {
                            closePopup();
                        }
                    }}
                >
                    <div className="crawler-popup">
                        <button
                            className="close-btn"
                            aria-label="Close popup"
                            onClick={closePopup}
                            type="button"
                        >×</button>
                        <h3>Crawl through website</h3>
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label>Start URL</label>
                                <input
                                    type="text"
                                    value={formData.startUrl}
                                    onChange={(e) => setFormData({ ...formData, startUrl: e.target.value })}
                                    placeholder="www.example.com"
                                    required
                                />
                            </div>

                            <div className="button-group">
                                <button
                                    type="button"
                                    onClick={closePopup}
                                    disabled={loading}
                                >
                                    Cancel
                                </button>
                                <button type="submit" disabled={loading}>
                                    {loading ? 'Warte auf Server...' : 'Start Crawler'}
                                </button>
                            </div>
                        </form>

                        {loading && (
                            <div className="loading-spinner">
                                <Spinner />
                            </div>
                        )}

                        {message && <div className="status-message">{message}</div>}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CrawlerPopup;
