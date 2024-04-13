
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms, send
from uuid import uuid4
import time
import random
import string

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

serverRooms = {}

def add_move(room_id, socket_id, move):
    print(serverRooms)
    room = serverRooms[room_id]

    if socket_id not in room['users_moves']:
        room['users_moves'][socket_id] = [move]
    else:
        room['users_moves'][socket_id].append(move)

def undo_move(room_id, socket_id):
    room = serverRooms[room_id]
    room['users_moves'][socket_id].pop()

def send_room_state(room_id, socket_id):
    room = serverRooms[room_id]
    moves = room['users_moves']
    socketio.emit('room_state', moves, room=socket_id)

@app.route('/hello')
def hello():
    return 'Hello World'

@socketio.on('create_room')
def on_create_room(data):
    # print(f"Received data on 'create_room': {data}")
    client_data = data['clientData']
    username = client_data['username']
    room_id = client_data['roomId']

    join_room(room_id)
    send(username + ' has entered the room.', to=room_id)
    serverRooms[room_id] = {
        'users_moves': {request.sid: []},
        'drawed': [],
        'users': {request.sid: username},
    }

    emit('created', room_id, room=request.sid)

@socketio.on('check_room')
def on_check_room(data):
    room_id = data
    emit('room_exists', room_id in serverRooms)

@socketio.on('join_room')
def on_join_room(data):
    # print(f"Received data on 'join_room': {data}")
    client_data = data['clientData']
    username = client_data['username']
    room_id = client_data['roomId']

    # commented out to implement later
    # if room and len(room['users']) < 12:
    join_room(room_id)
    send_room_state(room_id, request.sid)

    serverRooms[room_id]['users'][request.sid] = username  # Fix here
    serverRooms[room_id]['users_moves'][request.sid] = []  # And here

    emit('joined', room_id, room=request.sid)
    # else:
    #     emit('joined', '', True, room=request.sid)

# @socketio.on('leave_room')
# def on_leave_room():
#     room_id = rooms(request.sid)[0]
#     leave_room(room_id)

#     emit('user_disconnected', request.sid, room=room_id)

@socketio.on('draw')
def on_draw(data):
    print(f"Received data on 'draw': {data} ")
    room_id = data['roomId']
    move = data

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
    # print(f"Received data on 'mouse_move': {data}")
    client_data = data['mousePos']
    x = client_data['x']
    y = client_data['y']
    print(f"this is the request.sid: {request.sid}")
    print(f"these are the rooms: {rooms}")
    if(rooms(request.sid)):
        print(f"this is the room: {rooms(request.sid)}")
    room_id = rooms(request.sid)[0]  # get the room id associated with the current sid

    emit('mouse_moved', {'newX': x, 'newY': y, 'socketIdMoved': rooms(request.sid)[0]})

@socketio.on('send_msg')
def on_send_msg(data):
    print(f"this is the message data: {data}")
    room_id = rooms(request.sid)[0]
    msg = {
        'userId': request.sid,
        'msg': data
    }

    # emit('new_msg', request.sid, msg, room=request.sid)
    emit('new_msg', msg)

@socketio.on('disconnect')
def on_disconnect():
    room_id = rooms(request.sid)[0]
    leave_room(room_id)

    emit('user_disconnected', request.sid, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)