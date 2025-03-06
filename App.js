import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import './App.css';

// Initialize Socket.IO
const socket = io('http://localhost:3001'); // Backend URL

function App() {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);

  // Listen for bot messages
  useEffect(() => {
    socket.on('bot message', (msg) => {
      setMessages((prev) => [...prev, { text: msg, sender: 'bot' }]);
    });

    return () => {
      socket.off('bot message');
    };
  }, []);

  const handleSend = () => {
    if (userInput.trim()) {
      // Emit user message to the server
      socket.emit('user message', userInput);
      setMessages((prev) => [...prev, { text: userInput, sender: 'user' }]);
      setUserInput('');
    }
  };

  return (
    <div className="app-container">
      <h1 className="main-heading">Medical Assistant Chatbot</h1>

      <div className="chatbox-container">
        <div className="messages-container">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={msg.sender === 'bot' ? 'bot-message' : 'user-message'}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your message..."
            className="input-field"
          />
          <button onClick={handleSend} className="send-button">Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
