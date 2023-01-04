import logo from './logo.svg';
import './App.css';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    const fetchAllMatches = async () => {
      const response = await fetch('http://localhost:8000/sports/football/matches');
      const data = await response.json();
      console.log(data);
    }
  
    const interval = setInterval(fetchAllMatches, 5000);
  
    return () => clearInterval(interval);
  
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
