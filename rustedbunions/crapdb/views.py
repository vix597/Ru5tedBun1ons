import threading
from uuid import uuid4
from datetime import timedelta
from datetime import datetime

from django.http import HttpResponse
from django.template import loader

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
        # TODO: Validate against something
        return None

        # Return the new session
        # return cls(username, password)

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
    template = loader.get_template('crapdb/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    context = {"success": False}

    index_template = loader.get_template("crapdb/index.html")
    if request.POST:
        d = request.POST.dict()
        username = d.get("username", None)
        password = d.get("password", None)
        print("Login: ", username, ":", password, sep='')

        if username is not None and password is not None:
            session = Session.validate(username, password)
            if session is not None:
                context["success"] = True
                context["session_id"] = session.oid
    else:
        context["success"] = True

    return HttpResponse(index_template.render(context, request))

def forgetful(request):
    template = loader.get_template('crapdb/forgetful.html')
    context = {}
    return HttpResponse(template.render(context, request))

def searchcrap(request):
    context = {"success": False}

    forgetful_template = loader.get_template("crapdb/forgetful.html")
    if request.POST:
        d = request.POST.dict()
        username = d.get("username", None)
        print("Search user: ", username)

        if username is not None:
            pass # Search the database (don't do any sanitization)
    else:
        context["success"] = None

    return HttpResponse(forgetful_template.render(context, request))
