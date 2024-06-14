import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');

  const sendMessage = async () => {
    try {
      const res = await axios.get('http://localhost:8000/chat', {
        params: { text: message }
      });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
    }
  };

  const login = async () => {
    try {
      const res = await axios.post('http://localhost:8000/token', {
        username, password
      });
      setToken(res.data.access_token);
    } catch (error) {
      console.error(error);
    }
  };

  const addData = async () => {
    try {
      await axios.post('http://localhost:8000/admin/add_data', {
        text: message
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Data added successfully');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>AI Chatbot</h1>
      <div>
        <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
        <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
        <button onClick={login}>Login</button>
      </div>
      <div>
        <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Your message" />
        <button onClick={sendMessage}>Send</button>
        <button onClick={addData}>Add Data</button>
      </div>
      <div>
        <p>Response: {response}</p>
      </div>
    </div>
  );
}

export default App;
