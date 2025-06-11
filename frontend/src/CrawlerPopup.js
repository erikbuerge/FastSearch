import React, { useState } from 'react';

import './App.css'

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

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/api/crawl', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    CRAWLER_START_URL: formData.startUrl,
                    CRAWLER_DEPTH: formData.depth,
                    KEYWORDS_MIN_LENGTH: formData.minLength,
                    KEYWORDS_MAX_AMOUNT: formData.maxAmount
                })
            });

            if (!response.ok) throw new Error('Request failed');
            const data = await response.json();
            setMessage(data.message || 'Crawler started successfully');
            setTimeout(() => closePopup(), 2000);
        } catch (error) {
            setMessage(error.message || 'Error starting crawler');
        } finally {
            setLoading(false);
        }
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
                            onClick={() => closePopup()}
                            type="button"
                        >×</button>
                        <h3>Crawl through website</h3>
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label>Start URL</label>
                                <input
                                    type="url"
                                    value={formData.startUrl}
                                    onChange={(e) => setFormData({...formData, startUrl: e.target.value})}
                                    placeholder="https://www.example.com"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Crawl depth</label>
                                <input
                                    type="number"
                                    value={formData.depth}
                                    onChange={(e) => setFormData({...formData, depth: e.target.value})}
                                    placeholder="2"
                                    min="1"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Minimum keyword length</label>
                                <input
                                    type="number"
                                    value={formData.minLength}
                                    onChange={(e) => setFormData({...formData, minLength: e.target.value})}
                                    placeholder="4"
                                    min="1"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Maximum keywords</label>
                                <input
                                    type="number"
                                    value={formData.maxAmount}
                                    onChange={(e) => setFormData({...formData, maxAmount: e.target.value})}
                                    placeholder="60"
                                    min="1"
                                    max="100"
                                    required
                                />
                            </div>

                            <div className="button-group">
                                <button
                                    type="button"
                                    onClick={() => closePopup()}
                                    disabled={loading}
                                >
                                    Cancel
                                </button>
                                <button type="submit" disabled={loading}>
                                    {loading ? 'Starting...' : 'Start Crawler'}
                                </button>
                            </div>
                        </form>

                        {message && <div className="status-message">{message}</div>}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CrawlerPopup;
