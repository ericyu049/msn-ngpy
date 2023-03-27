import socketio
import eventlet
import time

sio = socketio.Server(logger=False, cors_allowed_origins=[
                      'http://localhost:4200'])

clients = {}
messages = []
# Connect user to the socket.IO server, add the user to the clients map.


@sio.on('connect')
def connect(sid, environ):
    print('Connected: ', sid)
    clients[sid] = ''

# Disconnect user from the socket.IO server, and remove them from the clients map.


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    del clients[sid]
    sio.emit('client_results', clients)

# Return a map containing all the connected users.


@sio.on('clients')
def getClients(sid):
    sio.emit('client_results', clients)

# Setting a nickname for the connected user.


@sio.on('setNickname')
def setNickname(sid, newname):
    clients[sid] = newname

# Getting the nickname of the connected user.


@sio.on('getNickname')
def getNickname(sid):
    return clients[sid]

# A message function. sid is the sender. This function will use send to broadcast the message data to the target.


@sio.on('send_message')
def message(sid, data, target):
    sender = {'sid': sid, 'nickname': clients[sid]}
    sio.send({'sender': sender, 'message': data}, to=target)
    if target != 'lobby':
        sio.send({'sender': sender, 'message': data}, to=sid)
    record = {'timestamp': time.time(), 'sender': sender, 'to': target,
              'message': data}
    messages.append(record)


# send a nudge to target client

@sio.on('nudge')
def nudge(sid, target):
    print('nudge target: ', target)
    sender = {'sid': sid, 'nickname': clients[sid]}
    sio.emit('got_nudged', {'sender': sender}, room=target['sid'])


# Enter the user to the main lobby.


@sio.on('enter_lobby')
def enterLobby(sid):
    print(sid, 'has entered the chat.')
    sio.enter_room(sid, 'lobby')

# Getting message history based on the target room.


@sio.on('history')
def getMessageHistory(sid, target):
    if target == 'lobby':
        result_messages = list(
            filter(lambda message: (message['to'] == 'lobby'), messages))
        return result_messages
    else:
        result_messages = list(filter(lambda message: ((message['to'] == sid and message['sender']['sid'] == target) or (
            message['sender']['sid'] == sid and message['to'] == target)), messages))
        return result_messages


# Main method.
if __name__ == '__main__':
    print('Starting SocketIO server...')
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
