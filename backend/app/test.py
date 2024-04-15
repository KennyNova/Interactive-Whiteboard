from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms, send
import uuid
from typing import Dict, List, Tuple, Any  # For type hinting

from objects import ClientToServerEvents, Move, Room, ServerToClientEvents

app = Flask(__name__)
socketio = SocketIO(app)
rooms: Dict[str, Room] = {}  # Type hint for clarity


def get_room_id(socket) -> str:  # Helper function
    joined_room = next((room for room in socket.rooms if room != socket.id), socket.id)
    return joined_room


def add_move(room_id: str, socket_id: str, move: Move):
    room = rooms.get(room_id)
    if room:
        if socket_id not in room['users_moves']:
            room['users_moves'][socket_id] = []
        room['users_moves'][socket_id].append(move)


def undo_move(room_id: str, socket_id: str):
    room = rooms.get(room_id)
    if room:
        room['users_moves'][socket_id].pop()


@socketio.on('connection')
def on_connect(socket):

@socketio.on('create_room')
def create_room(username: str):
    room_id = str(uuid.uuid4())[:6]  # Simplified room ID generation
    join_room(room_id)
    rooms[room_id] = {
        'users_moves': {},
        'drawed': [],
        'users': {socket.id: username}
    }
    emit('created', room_id, to=socket.id)

@socketio.on('check_room')
def check_room(room_id: str):
    emit('room_exists', room_id in rooms, to=socket.id)

@socketio.on('join_room')
def join_room(room_id: str, username: str):
    room = rooms.get(room_id)
    if room and len(room['users']) < 12:
        join_room(room_id)
        room['users'][socket.id] = username
        room['users_moves'][socket.id] = []
        emit('joined', room_id, to=socket.id)
    else:
        emit('joined', '', True, to=socket.id)  # Indicate failure

@socketio.on('joined_room')
def joined_room():
    room_id = get_room_id(socket)
    room = rooms.get(room_id)
    if room:
        # You'll need stringify logic for users_moves, users similar to the JS side
        emit('room', room, 'users_moves_stringified', 'users_stringified', to=socket.id)
        socket.broadcast.to(room_id).emit('new_user', socket.id, room['users'].get(socket.id) or 'Anonymous')

@socketio.on('leave_room')
def leave_room():
    room_id = get_room_id(socket)
    if room_id in rooms:
        user_moves = rooms[room_id]['users_moves'].get(socket.id)
        if user_moves:
            rooms[room_id]['drawed'].extend(user_moves)
        del rooms[room_id]['users'][socket.id]

    leave_room(room_id)
    socket.broadcast.to(room_id).emit('user_disconnected', socket.id)

@socketio.on('draw')
def draw(move: Move):
    room_id = get_room_id(socket)
    move['id'] = str(uuid.uuid4()) # Assign an ID
    add_move(room_id, socket.id, move)
    timestamp = move.pop('timestamp', None)  # Extract timestamp if present

    emit('your_move', move, timestamp=timestamp, to=socket.id) 
    socket.broadcast.to(room_id).emit('user_draw', move, timestamp=timestamp, room=room_id) 

@socketio.on('undo')
def undo():
    room_id = get_room_id(socket)
    undo_move(room_id, socket.id)
    socket.broadcast.to(room_id).emit('user_undo', socket.id)

@socketio.on('mouse_move')
def mouse_move(x: float, y: float):  # Assuming coordinates are floats
    room_id = get_room_id(socket)
    socket.broadcast.to(room_id).emit('mouse_moved', x, y, socket.id)

@socketio.on('send_msg')
def send_msg(msg: str):
    room_id = get_room_id(socket)
    # You might want to add message processing/formatting logic here
    socket.broadcast.to(room_id).emit('new_msg', socket.id, msg) 


@app.route('/hello')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    socketio.run(app, debug=True)
