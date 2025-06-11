import React from 'react';
import './App.css';
import SearchBar from './SearchBar';

function App() {
  return (
      <div className="search-app">
        <header className="search-header">
          <img src="/icon.png" alt="Logo" className="search-logo" />
          <h1 className="search-title">FastSearch</h1>
          <SearchBar autoFocus />
        </header>
      </div>
  );
}

export default App;
