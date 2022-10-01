import models
import routes
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from models import Session
from threading import Lock
from shared_db import db
from custom import xor

app = Flask(__name__, static_url_path='', static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
# Create model for the session table
socketio = SocketIO(app, async_mode=None, cors_allowed_origins='*')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


with app.app_context():
    db.create_all()


thread = None
thread_lock = Lock()


def background_thread():
    while True:
        socketio.sleep(1)
        send_sessions()


@socketio.event
def connect():
    print('[+] Client connected')
    with thread_lock:
        global thread
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@socketio.event
def load(data):
    print("[-] Loading session {}".format(data['id']))
    with app.app_context():
        session = Session.query.filter_by(id=data['id']).first()
        if session is not None:
            # save file to the folder shellcode with the name of the session id & xor it
            with open("shellcode/{}.bin".format(session.id), "wb") as f:
                f.write(xor(data['file']))
            session.loaded = True
            db.session.commit()
            f.close()
            print("[+] Loaded shellcode")
        else:
            print("[!] Session not found")


def send_sessions():
    with app.app_context():
        sessions = Session.query.all()
        sessions = [session.serialize for session in sessions]
        socketio.emit('sessions', sessions)


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=8001, host="0.0.0.0")
