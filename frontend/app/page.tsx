'use client'

import { FormEvent, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { io} from 'socket.io-client';
import { useSetRoomId } from '@/components/room/room.hooks';

export default function Home() {
  const setAtomRoomId = useSetRoomId();

  const [roomId, setRoomId] = useState('');
  const [username, setUsername] = useState('');

  // const router = useRouter();

  const socket = io('http://localhost:8000');

  useEffect(() => {
    

    // Add event listeners and handle socket events here
    socket.on('connect', () => {
      console.log('Connected to backend');
    });

    socket.on('connect_error', (error: String) => {
      console.log('Connection Error', error);
    });
    
    socket.on('connect_timeout', (timeout: String) => {
      console.log('Connection Timeout', timeout);
    });
    


    socket.on('error', (error: String) => {
      console.log('Error', error);
    });
    
    socket.on('disconnect', (reason: String) => {
      console.log('Disconnected', reason);
    });
    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

  const handleJoinRoom = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    socket.emit('join_room', roomId, name);
  };

  const handleCreateRoom = () => {
    socket.emit('create_room', username);
  };

  return (
    <div className="flex flex-col items-center py-24">
      <h1 className="text-5xl font-extrabold leading-tight sm:text-extra">
        Collabio
      </h1>
      <h3 className="text-xl sm:text-2xl">Real-time whiteboard</h3>

      <div className="mt-10 flex flex-col gap-2">
        <label className="self-start font-bold leading-tight">
          Enter your name
        </label>
        <input
          className="input"
          id="room-id"
          placeholder="Username..."
          value={username}
          onChange={(e) => setUsername(e.target.value.slice(0, 15))}
        />
      </div>

      <div className="my-8 h-px w-96 bg-zinc-200" />

      <form
        className="flex flex-col items-center gap-3"
        onSubmit={handleJoinRoom}
      >
        <label htmlFor="room-id" className="self-start font-bold leading-tight">
          Enter room id
        </label>
        <input
          className="input"
          id="room-id"
          placeholder="Room id..."
          value={roomId}
          onChange={(e) => setRoomId(e.target.value)}
        />
        <button className="btn" type="submit">
          Join
        </button>
      </form>

      <div className="my-8 flex w-96 items-center gap-2">
        <div className="h-px w-full bg-zinc-200" />
        <p className="text-zinc-400">or</p>
        <div className="h-px w-full bg-zinc-200" />
      </div>

      <div className="flex flex-col items-center gap-2">
        <h5 className="self-start font-bold leading-tight">Create new room</h5>

        <button className="btn" onClick={handleCreateRoom}>
          Create
        </button>
      </div>
    </div>
  );
}