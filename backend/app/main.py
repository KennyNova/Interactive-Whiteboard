from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
from uuid import uuid4
import random
import string

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

def add_move(room_id, socket_id, move):
    room = rooms[room_id]

    if socket_id not in room['users_moves']:
        room['users_moves'][socket_id] = [move]
    else:
        room['users_moves'][socket_id].append(move)

def undo_move(room_id, socket_id):
    room = rooms[room_id]
    room['users_moves'][socket_id].pop()

@app.route('/hello')
def hello():
    return 'Hello World'

@socketio.on('create_room')
def on_create_room(data):
    username = data['username']
    room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    while room_id in rooms:
        room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    join_room(room_id)

    rooms[room_id] = {
        'users_moves': {request.sid: []},
        'drawed': [],
        'users': {request.sid: username},
    }

    emit('created', room_id, room=request.sid)

@socketio.on('check_room')
def on_check_room(data):
    room_id = data['room_id']
    emit('room_exists', room_id in rooms)

@socketio.on('join_room')
def on_join_room(data):
    room_id = data['room_id']
    username = data['username']

    room = rooms.get(room_id)

    if room and len(room['users']) < 12:
        join_room(room_id)

        room['users'][request.sid] = username
        room['users_moves'][request.sid] = []

        emit('joined', room_id, room=request.sid)
    else:
        emit('joined', '', True, room=request.sid)

@socketio.on('leave_room')
def on_leave_room():
    room_id = rooms(request.sid)[0]
    leave_room(room_id)

    emit('user_disconnected', request.sid, room=room_id)

@socketio.on('draw')
def on_draw(data):
    room_id = list(request.sid_rooms)[1]
    move = data['move']

    timestamp = int(time.time())

    move['id'] = str(uuid4())

    add_move(room_id, request.sid, {**move, 'timestamp': timestamp})

    emit('your_move', {**move, 'timestamp': timestamp}, room=request.sid)

    emit('user_draw', {**move, 'timestamp': timestamp}, room=room_id, include_self=False)

@socketio.on('undo')
def on_undo():
    room_id = list(request.sid_rooms)[1]

    undo_move(room_id, request.sid)

    emit('user_undo', request.sid, room=room_id, include_self=False)

@socketio.on('mouse_move')
def on_mouse_move(data):
    x = data['x']
    y = data['y']

    emit('mouse_moved', x, y, request.sid, room=list(request.sid_rooms)[1], include_self=False)

@socketio.on('send_msg')
def on_send_msg(data):
    msg = data['msg']

    emit('new_msg', request.sid, msg, room=list(request.sid_rooms)[1])

@socketio.on('disconnect')
def on_disconnect():
    room_id = rooms(request.sid)[0]
    leave_room(room_id)

    emit('user_disconnected', request.sid, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)