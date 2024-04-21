import { io, Socket } from 'socket.io-client';

import { ClientToServerEvents, ServerToClientEvents } from '../types/global';

export const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(process.env.REACT_APP_BACKEND_URL || "http://localhost:8000");