import socketio
import eventlet
import time

origins = ['http://localhost:4200', 'https://chat.ai-amadeus.com']
sio = socketio.Server(logger=False, cors_allowed_origins=origins)

clients = {}
messages = []
# Connect user to the socket.IO server, add the user to the clients map.


@sio.on('connect')
def connect(sid, environ):
    print('Connected: ', sid)
    clients[sid] = ('', '')

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
    clients[sid][0] = newname


# Setting custom message for the connected user
@sio.on('setCustomMessage')
def setCustomMessage(sid, customMessage):
    clients[sid][1] = customMessage


# Getting the nickname of the connected user.


@sio.on('getNickname')
def getNickname(sid):
    return clients[sid][0]

# Getting the custom message of the connected user


@sio.on('getCustomMessage')
def getCustomMessage(sid):
    return clients[sid][1]

# A message function. sid is the sender. This function will use send to broadcast the message data to the target.


@sio.on('send_message')
def message(sid, data, target):
    sender = {'sid': sid, 'nickname': clients[sid][0]}

    # Sends the message to the target room or target user.

    sio.send({'sender': sender, 'message': data,
             'isLobby': True, 'self_copy': False}, to=target)

    # If the target is not the lobby, sends a copy the message to the sender

    if target != 'lobby':
        sio.send({'sender': sender, 'message': data,
                 'isLobby': False, 'self_copy': True}, to=sid)

    record = {'timestamp': time.time(), 'sender': sender, 'to': target,
              'message': data}
    messages.append(record)


# send a nudge to target client

@sio.on('nudge')
def nudge(sid, target):
    sender = {'sid': sid, 'nickname': clients[sid][0]}
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
