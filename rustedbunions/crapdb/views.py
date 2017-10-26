import sqlite3
import json
import hashlib

from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.template import loader

from crapdb.session import Session
from rustedbunions import settings

from .models import Flag

def update_hacker_bucks_from_flag(session, userflag):
    '''
    Get flag points from the real database. This
    is actually done securely...no SQL injections
    here
    '''
    # Normalize input
    userflag = userflag.strip()
    hacker_bucks = 0
    matched_flag = None
    try:
        #pylint: disable=E1101
        for flagentry in Flag.objects.all():
            flag = flagentry.flag

            # Check if it's equal
            if userflag == flag:
                hacker_bucks = flagentry.value
                matched_flag = flag

            # If not, see if they just submitted the flag
            # value b/w curly braces
            flag = flag.replace("Flag={", '')
            flag = flag.replace("}", '')
            if userflag == flag:
                hacker_bucks = flagentry.value
                matched_flag = flag
    except:
        pass

    if hacker_bucks and matched_flag:
        # If the flag hasn't already been claimed
        if matched_flag not in session.claimed_flags:
            session.claimed_flags.append(matched_flag)
            session.hacker_bucks += hacker_bucks
            session.lifetime_hacker_bucks += hacker_bucks

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

    context["session_id"] = session_id
    context["session"] = session.to_json()
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
            # Query that will filter out SQLi
            # because the user values are passed to execure as parameters
            no_sqli_query = ' '.join((
                "SELECT password FROM users",
                "WHERE username=? COLLATE NOCASE",
                "AND answer=?"
            ))

            # This query is suceptible to SQLi b/c user values are concatenated
            # to the string
            query = ' '.join((
                "SELECT password FROM users",
                "WHERE username='" + username + "' COLLATE NOCASE",
                "AND answer='" + answer + "'"
            ))

            context["actually_valid"] = False
            try:
                res = [x for x in cursor.execute(no_sqli_query, (username, answer))]
                if res:
                    # They got it right with no SQLi
                    context["actually_valid"] = True

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
        Session.get_session(session_id)
    except KeyError:
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

    # NOTE: Change this flag before deploy
    return HttpResponse(json.dumps({
        "flag": "Flag={__PLACEHOLDER_FLAG__}"
    }))

def querydb(request, session_id):
    try:
        Session.get_session(session_id)
    except KeyError:
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

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
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

    ret = {"hacker_bucks": session.hacker_bucks}

    if request.POST:
        d = request.POST.dict()
        flag = d.get("flag", None)

        if flag is not None:
            # Set's the session's hacker_bucks and prevents
            # getting points for the same flag more than once
            update_hacker_bucks_from_flag(session, flag)
            ret["hacker_bucks"] = session.hacker_bucks

    return HttpResponse(json.dumps(ret))

def getpin(request, session_id):
    PIN_PRICE = 15 # 15 hacker bucks to get the pin
    
    try:
        session = Session.get_session(session_id)
    except KeyError:
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

    if session.hacker_bucks < PIN_PRICE:
        return HttpResponse(json.dumps({
            "error": "Brutal force requires ${} hacker bucks to play".format(
                PIN_PRICE
            )
        }))

    # Charge the hacker bucks
    session.hacker_bucks -= PIN_PRICE

    ret = {
        "pin_hash": hashlib.md5(str(session.pin).encode('utf-8')).hexdigest(),
        "hacker_bucks": session.hacker_bucks
    }
    return HttpResponse(json.dumps(ret))

def getpinflag(request, session_id):
    try:
        session = Session.get_session(session_id)
    except KeyError:
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

    ret = {}

    if request.POST:
        d = request.POST.dict()
        pin = d.get("pin", None)

        if pin is not None:
            try:
                pin = int(pin)
                if pin < 1 or pin > 9999:
                    raise ValueError()

                if pin == session.pin:
                    # NOTE: Change this value before deploy
                    ret = {
                        "flag": "Flag={__PLACEHOLDER_FLAG__}"
                    }
            except ValueError:
                ret = {
                    "error": "Provided PIN is not a valid integer in the range 1 - 9999"
                }
        else:
            ret = {"error": "No PIN provided in POST request"}

    return HttpResponse(json.dumps(ret))

def getencmsg(request, session_id):
    ENC_PRICE = 50

    try:
        session = Session.get_session(session_id)
    except KeyError:
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

    if session.hacker_bucks < ENC_PRICE:
        return HttpResponse(json.dumps({
            "error": "ROT? requires ${} hacker bucks to play".format(
                ENC_PRICE
            )
        }))

    # Charge the hacker bucks
    session.hacker_bucks -= ENC_PRICE

    ret = {
        "encrypted_message": session.encrypted_message,
        "hacker_bucks": session.hacker_bucks
    }
    return HttpResponse(json.dumps(ret))

def getrotflag(request, session_id):
    try:
        session = Session.get_session(session_id)
    except KeyError:
        return HttpResponse(json.dumps({
            "redirect": "No session or session expired."}))

    ret = {}

    if request.POST:
        d = request.POST.dict()
        answer = d.get("answer", None)

        if answer is not None:
            print("***CHECK: ", answer.strip().lower(), " ***AND*** ", session.message)
            if answer.strip().lower() == session.message:
                # NOTE: Change this value before deploy
                ret = {
                    "flag": "Flag={__PLACEHOLDER_FLAG__}"
                }
            else:
                ret = {
                    "error": "Provided answer does not match"
                }
        else:
            ret = {"error": "No answer provided in POST request"}

    return HttpResponse(json.dumps(ret))
