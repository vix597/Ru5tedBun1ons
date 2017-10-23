import sqlite3
import json

from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.template import loader

from crapdb.session import Session
from rustedbunions import settings

from .models import Flag

def get_flag_points(userflag):
    '''
    Get flag points from the real database. This
    is actually done securely...no SQL injections
    here
    '''
    # Normalize input
    userflag = userflag.strip()

    try:
        #pylint: disable=E1101
        for flagentry in Flag.objects.all():
            flag = flagentry.flag
            if userflag == flag:
                return flagentry.value
            flag = flag.replace("Flag={", '')
            flag = flag.replace("}", '')
            if userflag == flag:
                return flagentry.value
    except:
        pass

    return 0

def index(request):
    context = {}

    if request.GET:
        d = request.GET.dict()
        context["error"] = d.get("error", None)

    template = loader.get_template('crapdb/index.html')
    return HttpResponse(template.render(context, request))

def main(request, session_id):
    context = {}
    session = None

    try:
        session = Session.get_session(session_id)
    except KeyError:
        return redirect(reverse("crapdb:index") + "?error={}".format(
            "Login failed. No session or session expired"))

    # Refresh the session so it doesn't expire
    session.update()

    context["session_id"] = session_id
    context["session"] = session
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

def getpassword(request):
    context = {}

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        username = d.get("username", None)
        answer = d.get("answer", None)

        if username is None or answer is None:
            context["error"] = "You must provide an answer"
        else:
            query = ' '.join((
                "SELECT password FROM users",
                "WHERE username='" + username + "' COLLATE NOCASE",
                "AND answer='" + answer + "'"
            ))
            try:
                context["password"] = [x for x in cursor.execute(query)]
                if not context["password"]:
                    context["error"] = "Wrong answer"
            except Exception as e:
                context["error"] = "'{}' - {}".format(query, str(e))

        conn.close()

    template = loader.get_template("crapdb/forgetful.html")
    return HttpResponse(template.render(context, request))

def searchcrap(request):
    context = {}

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        username = d.get("username", None)

        if username is not None:
            query = "SELECT username, question FROM users WHERE username='" + username + "' COLLATE NOCASE"
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

def getmodalflag(request, session_id):
    try:
        session = Session.get_session(session_id)
    except KeyError:
        return redirect(reverse("crapdb:index") + "?error={}".format(
            "No session or session expired"))

    # Refresh the session so it doesn't expire
    session.update()

    # NOTE: Change this flag before deploy
    return HttpResponse(json.dumps({
        "flag": "Flag={__PLACEHOLDER_FLAG__}"
    }))

def querydb(request, session_id):
    try:
        session = Session.get_session(session_id)
    except KeyError:
        return redirect(reverse("crapdb:index") + "?error={}".format(
            "No session or session expired"))

    # Refresh the session so it doesn't expire
    session.update()

    ret = {"flags": []}

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        query = d.get("query", None)

        if query is not None:
            try:
                ret["flags"] = [x for x in cursor.execute(query)]
                if not ret["flags"]:
                    ret["error"] = "No flags found in database"
            except Exception as e:
                ret["error"] = "'{}' - {}".format(query, str(e))

        conn.close()

    return HttpResponse(json.dumps(ret))

def checkflag(request, session_id):
    try:
        session = Session.get_session(session_id)
    except KeyError:
        return redirect(reverse("crapdb:index") + "?error={}".format(
            "No session or session expired"))

    # Refresh the session so it doesn't expire
    session.update()

    ret = {"points": 0}

    if request.POST:
        d = request.POST.dict()
        flag = d.get("flag", None)

        if flag is not None:
            ret["points"] = get_flag_points(flag)

    return HttpResponse(json.dumps(ret))
