# MSN Server

This project is a python server for the recreation of the classic Windows live messenger. This server utilizes python-socketio, a python version of Socket.IO library to handle all connections and events as well as broadcasting functions for client messenging.

## How to run

Make sure you have Python3 installed and all required dependencies

Inside the ```server.py```, line 5  has a array that looks like this: 
```origins = ['http://localhost:4200', 'https://chat-ai-amadeus.com']```.

This contains a list of all the allowed origins. If you are running the clients locally on multiple machines and the domain is anything different from the provided list, add the machine's host ip addresses to the array, separated by comma.

Then, run
``` python3 server.py ```



Refer to ```server.py``` to see all availble events that the server can handle.


