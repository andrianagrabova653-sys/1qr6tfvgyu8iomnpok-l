import socketio, threading

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('message')
def on_message(data):
    print(f"Received message: {data}")


def send_message():
    while True:
        message = input()
        if message == "/exit":
            sio.disconnect()
            break




sio.connect("http://192.168.0.100:5000",
            auth={'name': input('enter ur username: ')})

threading.Thread(target=send_message, daemon=True).start()


sio.wait()