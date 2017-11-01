import sqlite3
import threading
import time
import random
import string
import os
from uuid import uuid4
from datetime import datetime
from datetime import timedelta

from rustedbunions import settings

MOVIE_QUOTES = []

# Load all the movie quotes
with open(os.path.join(settings.BASE_DIR, "movie_quotes.txt")) as f:
    MOVIE_QUOTES.extend(f.readlines())

class Session:
    _registry = {}
    _session_lock = threading.Lock()
    SESSION_TIMEOUT = 30 # 30 minute session timeout
    CLEANUP_EVENT = threading.Event()
    ALPHABET = string.ascii_lowercase

    @classmethod
    def get_session(cls, oid):
        with cls._session_lock:
            session = cls._registry.get(oid)
            if session and session.is_valid():
                session.update()
                return session
            elif session and not session.is_valid():
                del cls._registry[oid]

        raise KeyError("no session found that matched object id " + oid)

    def __init__(self, username, password, user_info=None):
        random.seed() # uses current system time
        self.username = username
        self.password = password
        self.hacker_bucks = 0
        self.lifetime_hacker_bucks = self.hacker_bucks
        self.claimed_flags = [] # The list of flags claimed
        self.actually_valid = False # True if the session resulted from no SQLi
        self.pin = random.randint(1337, 9999) # The user's random PIN number
        self.key = random.randint(1, 25) # pick a random shift b/w 1 and 25
        self.message = MOVIE_QUOTES[random.randint(0, len(MOVIE_QUOTES))].strip().lower()
        self.encrypted_message = self.shifttext(self.key, self.message)
        self.user_info = user_info or []
        self.oid = str(uuid4()).replace('-', '')
        self.expires = datetime.utcnow() + timedelta(minutes=self.SESSION_TIMEOUT)

        # Determines if this is actually a valid login or not
        # This will set self.actually_valid accordingly
        self.secure_validate()

        with Session._session_lock:
            Session._registry[self.oid] = self

    def to_json(self):
        '''
        Leaves out the secrets that should remain on the server
        '''
        return {
            "username": self.username,
            "password": self.password,
            "hacker_bucks": self.hacker_bucks,
            "user_info": self.user_info,
            "oid": self.oid,
            "expires": self.expires,
            "actually_valid": self.actually_valid
        }

    def update(self):
        if self.is_valid():
            self.expires = datetime.utcnow() + timedelta(minutes=self.SESSION_TIMEOUT)

    def is_valid(self):
        check = datetime.utcnow()
        if check < self.expires:
            return True
        else:
            return False

    def shifttext(self, shift, msg):
        msg = msg.strip().lower()
        data = []
        for c in msg:
            if c.strip() and c in self.ALPHABET:
                data.append(self.ALPHABET[(self.ALPHABET.index(c) + shift) % 26])
            else:
                data.append(c)

        output = ''.join(data)
        return output

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
            # Every 5 minutes cleanup sessions
            time.sleep(300)
            with Session._session_lock:
                rem_oids = []
                for session in Session._registry.values():
                    if not session.is_valid():
                        print("Found expired session: ", session.oid)
                        rem_oids.append(session.oid)
                for oid in rem_oids:
                    del Session._registry[oid]

        print("Session cleanup monitor complete.")
