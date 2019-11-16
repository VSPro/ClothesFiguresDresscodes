import React from 'react';
import logo from './logo.svg';
import './App.css';

import TestContainer from '../TestContainer/TestContainer'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <TestContainer />
      </header>
    </div>
  );
}

export default App;
