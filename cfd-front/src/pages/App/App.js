import React from 'react';
import logo from './logo.svg';
import './App.css';

import TestContainer from '../TestContainer/'

function App( props ) {
  
  console.log('I\'m called from App component', props)
  
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
