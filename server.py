from flask import Flask, request
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
socketio = SocketIO(app, 
                    cors_allowed_origins="*", 
                    async_mode="eventlet")

clients = []

def getName(clients, id):
    for element in clients:
        for key in element:
            if key == id:
                return element[key]['name']

@socketio.on("connect")
def handle_connect(auth):
    newUser = {request.sid: auth}
    clients.append(newUser)
    print(f"✅ Клієнт {request.sid} доєднався!")
    print(clients)

@socketio.on("disconnect")
def handle_disconnect():
    print(f"❌ Клієнт {request.sid} відключився")

@socketio.on("message")
def handle_message(msg):
    print(f"📩 Отримано нове повідомлення від {getName(clients, request.sid)}: {msg[0]}")
    send(f"{getName(clients, request.sid)}: {msg[0]}", broadcast=True)  # відправка всім клієнтам


print("🚀 Сервер почав роботу")
portServer = int(os.environ.get("PORT", 5000))
socketio.run(app, host="0.0.0.0", port=portServer)