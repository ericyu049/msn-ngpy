import socketio
import eventlet

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


@sio.on('getClientslist')
def getClients(sid):
    sio.emit('client_results', clients)

# Setting a nickname for the connected user.


@sio.on('setNickname')
def setNickname(sid, newname):
    clients[sid] = newname

# Getting the nickname of the connected user.


@sio.on('getNickname')
def getNickname(sid):
    sio.emit('receiveNickname', clients[sid], room=sid)

# A message function. sid is the sender. This function will use send to broadcast the message data to the target.


@sio.on('send_message')
def message(sid, data, target):
    sender = {'sid': sid, 'nickname': clients[sid]}
    sio.send({'sender': sender, 'message': data}, to=target)

# Enter the user to the main lobby.


@sio.on('enter_lobby')
def enterLobby(sid):
    print(sid, 'has entered the chat.')
    sio.enter_room(sid, 'lobby')

# Send a message to the main lobby.


@sio.on('message_lobby')
def messageLobby(sid, data):
    sio.emit('lobby_message', {'sender': sid, 'message': data}, room='lobby')

# Receive messages


# Main method.
if __name__ == '__main__':
    print('Starting SocketIO server...')
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
