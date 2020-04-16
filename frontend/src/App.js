import React from 'react';
import './App.css';
import NavigationBar from './NavigationBar';
import FrontPage from './FrontPage'

function App() {
  return (
    <div>
      <NavigationBar 
        current={0} 
      />
      <FrontPage />
    </div>
  );
}

export default App;
