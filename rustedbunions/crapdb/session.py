import sqlite3
import threading
import time
from uuid import uuid4
from datetime import datetime
from datetime import timedelta

from rustedbunions import settings

class Session:
    _registry = {}
    _session_lock = threading.Lock()
    SESSION_TIMEOUT = 30 # 30 minute session timeout
    CLEANUP_EVENT = threading.Event()

    @classmethod
    def get_session(cls, oid):
        session = cls._registry.get(oid)
        if session and session.is_valid():
            session.update()
            return session

        raise KeyError("no session found that matched object id " + oid)

    def __init__(self, username, password, user_info=None):
        self.username = username
        self.password = password
        self.hacker_bucks = 0
        self.claimed_flags = [] # The list of flags claimed
        self.actually_valid = False # True if the session resulted from no SQLi
        self.user_info = user_info or []
        self.oid = str(uuid4()).replace('-', '')
        self.expires = datetime.utcnow() + timedelta(minutes=self.SESSION_TIMEOUT)

        # Determines if this is actually a valid login or not
        # This will set self.actually_valid accordingly
        self.secure_validate()

        with Session._session_lock:
            Session._registry[self.oid] = self

    def update(self):
        if self.is_valid():
            self.expires = datetime.utcnow() + timedelta(minutes=self.SESSION_TIMEOUT)

    def is_valid(self):
        check = datetime.utcnow()
        if check < self.expires:
            return True
        else:
            return False

    @classmethod
    def validate(cls, username, password):
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()
        query = ' '.join((
            "SELECT username, password FROM users",
            "WHERE username='" + username + "' COLLATE NOCASE",
            "and password='" + password + "'"
        ))
        result = []

        try:
            result = [x for x in cursor.execute(query)]
        except Exception as e:
            conn.close()
            raise Exception("'{}' - {}".format(query, str(e)))

        conn.close()

        if result:
            return cls(username, password, user_info=result)
        else:
            return None

    def secure_validate(self):
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()
        
        query = ' '.join((
            "SELECT username, password FROM users",
            "WHERE username=? COLLATE NOCASE",
            "and password=?"
        ))

        result = None
        try:
            result = [x for x in cursor.execute(query, (self.username, self.password))]
        except:
            pass

        conn.close()

        if result:
            self.actually_valid = True
        else:
            self.actually_valid = False

    @classmethod
    def logout(cls, session_id):
        with cls._session_lock:
            if session_id in cls._registry:
                del cls._registry[session_id]

    @staticmethod
    def cleanup():
        '''
        Runs in a thread and cleans up expired sessions
        '''
        print("Session cleanup monitor running...")

        while not Session.CLEANUP_EVENT.is_set():
            # Every 1 second cleanup sessions
            time.sleep(1)
            with Session._session_lock:
                rem_oids = []
                for session in Session._registry.values():
                    if not session.is_valid():
                        print("Found expired session: ", session.oid)
                        rem_oids.append(session.oid)
                for oid in rem_oids:
                    del Session._registry[oid]

        print("Session cleanup monitor complete.")
