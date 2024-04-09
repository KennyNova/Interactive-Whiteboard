import React, { useState, useEffect } from 'react';
import Whiteboard from './Whiteboard';
import io from 'socket.io-client';

const Room: React.FC = ({ roomId }) => {
  const [socket, setSocket] = useState<SocketIOClient.Socket | null>(null);

  useEffect(() => {
    const newSocket = io('http://localhost:your_backend_port'); // Replace with actual backend URL
    setSocket(newSocket);

    // Handle socket events for sending and receiving whiteboard updates
    newSocket.on('update', (data) => {
      // Update Tldraw state based on received data
    });

    return () => newSocket.disconnect();
  }, [roomId]);

  return (
    <div>
      <h1>Room: {roomId}</h1>
      <Whiteboard />
    </div>
  );
};

export default Room;