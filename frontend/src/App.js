import React from 'react';
import './App.css';

function App() {
  const handleClick = () => {
    if (window.Telegram && window.Telegram.WebApp) {
      const data = { message: "Hello from the mini app!" };
      window.Telegram.WebApp.sendData(JSON.stringify(data));
      window.Telegram.WebApp.close();
    } else {
      console.log("This app is not running inside Telegram.");
      alert("This app is not running inside Telegram.");
    }
  };

  return (
    <div className="App">
      <h1>Welcome to My Mini App!</h1>
      <p>This is a simple Telegram mini app built with React.</p>
      <button onClick={handleClick}>Click Me!</button>
    </div>
  );
}

export default App;