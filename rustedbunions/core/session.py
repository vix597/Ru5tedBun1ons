import sqlite3
import threading
import time
from datetime import datetime
from datetime import timedelta

from core.util import ObjectId
from rustedbunions import settings

class LoginSqlInjectionError(Exception):
    '''
    Exception thrown for SQL injection attempts at login
    '''
    pass

class Session:
    '''
    Base session class.
    '''

    _challenge_registry = {}
    _registry = {}
    _session_lock = threading.Lock()
    SESSION_TIMEOUT = 30 # 30 minute session timeout
    CLEANUP_EVENT = threading.Event()

    @classmethod
    def get_session(cls, oid, create=False):
        with cls._session_lock:
            session = cls._registry.get(oid)
            if session and session.is_valid():
                session.update()
                return session
            elif session and not session.is_valid():
                del cls._registry[oid]
        
        raise KeyError("no session found that matched object id " + oid)

    @classmethod
    def register_challenge(cls, challenge_cls):
        cls._challenge_registry[challenge_cls.meta.challenge_id] = challenge_cls

    def __init__(self, oid=None):
        self.oid = oid or ObjectId()
        self.hacker_bucks = 0
        self.lifetime_hacker_bucks = 0
        self.claimed_flags = []
        self.expires = datetime.utcnow() + timedelta(minutes=self.SESSION_TIMEOUT)
        self.challenges = {}

        # Load up unique versions of each challenge for this session
        for challenge_id, challenge_cls in self._challenge_registry.items():
            self.challenges[challenge_id] = challenge_cls()

        with self._session_lock:
            self._registry[self.oid] = self

    def to_json(self):
        return {
            "oid": self.oid,
            "hacker_bucks": self.hacker_bucks,
            "lifetime_hacker_bucks": self.lifetime_hacker_bucks,
            "expires": self.expires,
            "challenges": {cid: c.to_json() for cid, c in self.challenges.items()}
        }

    def get_challenge(self, challenge_id):
        return self.challenges.get(challenge_id, None)

    def from_other_session(self, other):
        self.claimed_flags = other.claimed_flags
        self.hacker_bucks = other.hacker_bucks
        self.lifetime_hacker_bucks = other.lifetime_hacker_bucks
        for other_challenge_id, other_challenge in other.challenges.items():
            self.challenges[other_challenge_id].from_other_challenge(other_challenge)

    def is_valid(self):
        check = datetime.utcnow()
        return check < self.expires

    def update(self):
        if self.is_valid():
            self.expires = datetime.utcnow() + timedelta(minutes=self.SESSION_TIMEOUT)

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

class UnauthenticatedSession(Session):
    '''
    Represents an unauthenticated session that stores hacker bucks between
    authenticated sessions
    '''

    def __init__(self, oid=None):
        super().__init__(oid=oid)

class AuthenticatedSession(Session):
    '''
    Represents an authenticated session that stores hacker bucks and challenges
    '''

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.actually_valid = False # True if the session resulted from no SQLi

        # Determines if this is actually a valid login or not
        # This will set self.actually_valid accordingly
        self.secure_validate()

    def to_json(self):
        '''
        Leaves out the secrets that should remain on the server
        '''
        d = super().to_json()
        d.update({
            "username": self.username,
            "password": self.password,
            "actually_valid": self.actually_valid
        })
        return d

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
            raise LoginSqlInjectionError("'{}' - {}".format(query, str(e)))

        conn.close()

        if result:
            return cls(username, password)
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
