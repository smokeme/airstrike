from datetime import datetime
from shared_db import db


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False, nullable=False)
    domain = db.Column(db.String, unique=False, nullable=False)
    machine = db.Column(db.String, unique=False, nullable=False)
    process = db.Column(db.String, unique=False, nullable=False)
    version = db.Column(db.String, unique=False, nullable=False)
    arch = db.Column(db.String, unique=False, nullable=False)
    ip = db.Column(db.String, unique=False, nullable=False)
    pid = db.Column(db.String, unique=False, nullable=False)
    loaded = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    method = db.Column(db.String, unique=False, nullable=True)
    kill = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    lastupdated = db.Column(db.DateTime, unique=False,
                            nullable=False, default=datetime.utcnow)

    @property
    def serialize(self):
        delayed = False
        # set delayed to true if the session lastupdated is more than 10 seconds ago
        if (datetime.utcnow() - self.lastupdated).total_seconds() > 10:
            delayed = True
        # Returns Data Object In Proper Format
        return {
            "id": self.id,
            "username": self.username,
            "domain": self.domain,
            "machine": self.machine,
            "process": self.process,
            "version": self.version,
            "arch": self.arch,
            "ip": self.ip,
            "pid": self.pid,
            "loaded": self.loaded,
            "method": self.method,
            "kill":self.kill,
            "delay":delayed,
            "lastupdated": str(int((datetime.utcnow() - self.lastupdated).total_seconds())) + " seconds"
        }
