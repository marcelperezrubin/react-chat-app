import io from 'socket.io-client';
import { useState, useEffect } from 'react';

const socket = io("/")

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newMessage = {
      body: message,
      from: 'Me'
    }

    setMessages([ ...messages, newMessage]);
    socket.emit('message', message);
  };

  useEffect(() => {
    socket.on("message",
      receiveMessage);

    return () => {
      socket.off("message", receiveMessage);
    }
  }, []);

  const receiveMessage = (message) =>
   setMessages((state) => [...state, message]);

  return (
    <div className="h-screen bg-zinc-800 text-white flex item-center
     justify-center">

    <form onSubmit={handleSubmit} className='bg-zinc-900 p-10'>
      <h1 className='text-2xl font-bold my-2'> Chat React App</h1>
      <input type="text" placeholder='Write your message...'
      className="border-2 border-zinc-500 p-2 w-full text-black" 
      onChange={(e) => setMessage(e.target.value)}
      />
      
      <button className='btn'>
        Send
      </button>
    </form>

    <ul>
      {
        messages.map((message, i) => (
          <li key={i}>
            {message.from}:{message.body}
            </li>
        ))
      }
    </ul>

    </div>
  );
}

export default App