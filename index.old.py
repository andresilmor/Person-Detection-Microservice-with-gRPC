#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
import time
import base64
import os
import io
import PIL.Image as Image

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)
    bytes = base64.b64decode(message)
    img = Image.open(io.BytesIO(bytes))
    img.show()
    #  Do some 'work'.
    #  Try reducing sleep time to 0.01 to see how blazingly fast it communicates
    #  In the real world usage, you just need to replace time.sleep() with
    #  whatever work you want python to do, maybe a machine learning task?
    time.sleep(0.01)

    #  Send reply back to client
    #  In the real world usage, after you finish your work, send your output here
    socket.send(b"World")


'''
import zmq
from flask import Flask
from threading import Thread

HOST = 'localhost'
PORT = 5000
TASK_SOCKET = zmq.Context().socket(zmq.REQ)
TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))
app = Flask("app")


@app.route("/start")
def start():
    TASK_SOCKET.send_json({"command": "start"})
    results = TASK_SOCKET.recv_json()
    return f"starting {results}"


@app.route("/pause")
def pause():
    TASK_SOCKET.send_json({"command": "pause"})
    results = TASK_SOCKET.recv_json()
    return f"pausing {results}"


class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self.active = True

    def run(self):
        self._socket.bind('tcp://{}:{}'.format(HOST, PORT))
        self._socket.setsockopt(zmq.RCVTIMEO, 500)
        while self.active:
            ev = self._socket.poll(1000)
            if ev:
                rec = self._socket.recv_json()
                self._socket.send_json({"response": "ok", "payload": rec})


if __name__ == "__main__":
    worker = Worker()
    worker.start()
    app.run()
    '''