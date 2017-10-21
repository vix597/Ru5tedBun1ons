import sqlite3
import threading
from uuid import uuid4
from datetime import timedelta
from datetime import datetime

from django.shortcuts import redirect
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
        self.oid = str(uuid4())
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
            raise Exception("'{}' - {}".format(query, str(e)))

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
    error = request.GET.get("error", None)
    print("***ERROR: ", error)
    template = loader.get_template('crapdb/index.html')
    context = {"error": error}
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('crapdb/main.html')
    context = {}
    d = request.GET.dict()
    try:
        Session.get_session(d.get("session_id", ""))
    except KeyError:
        return redirect("/?error=Invalid Session")

    return HttpResponse(template.render(context, request))

def login(request):
    context = {"success": False}
    template = loader.get_template("crapdb/index.html")

    if request.POST:
        d = request.POST.dict()
        username = d.get("username", None)
        password = d.get("password", None)
        print("Login: ", username, ":", password, sep='')

        if username is not None and password is not None:
            try:
                session = Session.validate(username, password)
                if session is not None:
                    return redirect("/crapdb/main/?session_id={}?username={}".format(
                        session.oid, username))
            except Exception as e:
                context["error"] = str(e)
    else:
        context["success"] = None

    return HttpResponse(template.render(context, request))

def logout(request):
    d = request.GET.dict()
    Session.logout(d.get("session_id", ""))
    return redirect("/")

def forgetful(request):
    template = loader.get_template('crapdb/forgetful.html')
    context = {}
    return HttpResponse(template.render(context, request))

def searchcrap(request):
    conn = sqlite3.connect(settings.CRAPDB_PATH)
    cursor = conn.cursor()
    context = {"success": False, "result": None}

    template = loader.get_template("crapdb/forgetful.html")
    if request.POST:
        d = request.POST.dict()
        username = d.get("username", None)
        print("Search user: ", username)

        if username is not None:
            context["success"] = True
            context["result"] = []
            query = "SELECT username, question FROM users WHERE username='" + username + "'"
            try:
                context["result"] = [x for x in cursor.execute(query)]
            except Exception as e:
                print("Exception: ", str(e))
                context["error"] = "'{}' - {}".format(query, str(e))
    else:
        context["success"] = None

    return HttpResponse(template.render(context, request))
