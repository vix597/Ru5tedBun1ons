import sqlite3
import threading
from uuid import uuid4
from datetime import timedelta
from datetime import datetime

from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.template import loader

from rustedbunions import settings

class Session:
    _registry = {}
    _session_lock = threading.Lock()

    @classmethod
    def get_session(cls, oid):
        session = cls._registry.get(oid)
        if session:
            return session

        raise KeyError("no session found that matched object id " + oid)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.oid = str(uuid4()).replace('-', '')
        self.expires = datetime.utcnow() + timedelta(minutes=5)

        with Session._session_lock:
            Session._registry[self.oid] = self

    def update(self):
        self.expires = datetime.utcnow() + timedelta(minutes=5)

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
            "WHERE username='" + username + "'",
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
            return cls(username, password)
        else:
            return None

    @classmethod
    def logout(cls, session_id):
        with cls._session_lock:
            if session_id in cls._registry:
                del cls._registry[session_id]

    @classmethod
    def cleanup(cls):
        with cls._session_lock:
            rem_oids = []
            for session in cls._registry.values():
                if not session.is_valid():
                    rem_oids.append(session.oid)
            for oid in rem_oids:
                del cls._registry[oid]

def index(request):
    context = {}

    if request.GET:
        d = request.GET.dict()
        context["error"] = d.get("error", None)

    template = loader.get_template('crapdb/index.html')
    return HttpResponse(template.render(context, request))

def main(request, session_id):
    context = {}

    try:
        Session.get_session(session_id)
    except KeyError:
        return redirect(reverse("crapdb:index") + "?error={}".format("Login failed. No Session"))

    context["session_id"] = session_id
    template = loader.get_template('crapdb/main.html')
    return HttpResponse(template.render(context, request))

def login(request):
    context = {}

    if request.POST:
        d = request.POST.dict()
        username = d.get("username", None)
        password = d.get("password", None)

        if username is not None and password is not None:
            try:
                session = Session.validate(username, password)
                if session is not None:
                    return redirect("crapdb:main", session_id=session.oid)
                else:
                    context["error"] = "Username/Password combination does not exist"
            except Exception as e:
                context["error"] = str(e)

    template = loader.get_template("crapdb/index.html")
    return HttpResponse(template.render(context, request))

def logout(request, session_id):
    Session.logout(session_id)
    return redirect("crapdb:index")

def forgetful(request):
    template = loader.get_template('crapdb/forgetful.html')
    context = {}
    return HttpResponse(template.render(context, request))

def searchcrap(request):
    context = {}

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        username = d.get("username", None)

        if username is not None:
            query = "SELECT username, question FROM users WHERE username='" + username + "'"
            try:
                context["result"] = [x for x in cursor.execute(query)]
                if not context["result"]:
                    context["error"] = "User not found in database"
            except Exception as e:
                context["error"] = "'{}' - {}".format(query, str(e))

        # Close the sqlite connection
        conn.close()

    template = loader.get_template("crapdb/forgetful.html")
    return HttpResponse(template.render(context, request))
