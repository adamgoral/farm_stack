import './App.css';
import { useEffect, useState } from 'react';

function App() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    const fetchAllMatches = async () => {
      const response = await fetch('http://localhost:8000/sports/football/matches');
      const data = await response.json();
      setMatches(data);
    }
  
    const interval = setInterval(fetchAllMatches, 5000);
  
    return () => clearInterval(interval);
  
  }, []);

  // Pass a function to map
  const items = matches.map(match => (<p>{match.home_team} vs {match.away_team} {match.home_goals}-{match.away_goals}</p>));
  return (
    <div className="App">
      <header className="App-header">
        {items}
      </header>
    </div>
  );
}

export default App;
