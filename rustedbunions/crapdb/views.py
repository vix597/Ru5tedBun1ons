import sqlite3
import json

from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader

from core.challenge import NotEnoughHackerBucksError, ChallengeNotSolvedError
from core.session import Session, AuthenticatedSession, LoginSqlInjectionError
from core.views import update_hacker_bucks_from_flag, get_session, get_unauth_session, FlagAlreadyClaimedError
from core.util import is_user_data_valid, DataType
from rustedbunions import settings
from flags import FlagGenerator

FLAGS = FlagGenerator.generate_flags()

#pylint: disable=E1101

def sync_session(request, session_id):
    ret = {}
    unauth_session = get_unauth_session(request)

    try:
        # Update the unauth session with the hacker bucks and flags
        session = Session.get_session(session_id)
        unauth_session.from_other_session(session)
    except KeyError:
        pass

    ret = {"hacker_bucks": unauth_session.hacker_bucks}
    return HttpResponse(json.dumps(ret))

def index(request):
    context = {
        "unauth_session": get_unauth_session(request).to_json(),
        "index_page_source": FLAGS["index_page_source"][0],
        "index_console_output": FLAGS["index_console_output"][0]
    }

    if request.GET:
        d = request.GET.dict()
        error = d.get("error", None)

        if not is_user_data_valid(error):
            context["error"] = "Too much data"
        else:
            context["error"] = error

    template = loader.get_template('crapdb/index.html')
    return HttpResponse(template.render(context, request))

def about(request):
    context = {"unauth_session": get_unauth_session(request).to_json()}
    template = loader.get_template('crapdb/about.html')
    return HttpResponse(template.render(context, request))

def main(request, session_id):
    context = {
        "no_user_login": FLAGS["no_user_login"][0],
        "no_password_login": FLAGS["no_password_login"][0],
        "valid_creds_login": FLAGS["valid_creds_login"][0],
        "shortest_sqli": FLAGS["shortest_sqli"][0]
    }
    status, obj = get_session(session_id, error="Login failed. No session or session expired")
    if not status:
        return obj # On fail obj is a redirect
    session = obj # On success obj is the session

    context["session_id"] = session_id
    context["session"] = session.to_json()
    template = loader.get_template('crapdb/main.html')
    return HttpResponse(template.render(context, request))

def login(request):
    context = {
        "index_page_source": FLAGS["index_page_source"][0],
        "index_console_output": FLAGS["index_console_output"][0]
    }
    unauth_session = get_unauth_session(request)

    if request.POST:
        d = request.POST.dict()
        username = d.get("username", None)
        password = d.get("password", None)

        if username is not None and password is not None:
            if not is_user_data_valid(username) or not is_user_data_valid(password):
                context["error"] = "Too much data"
            else:
                try:
                    session = AuthenticatedSession.validate(request, username, password)
                    if session is not None:
                        # Update the new session with the current hacker bucks and flags
                        session.from_other_session(unauth_session)
                        return redirect("crapdb:main", session_id=session.oid)
                    else:
                        context["error"] = "Username/Password combination does not exist"
                except LoginSqlInjectionError as e:
                    context["error"] = str(e)

    context["unauth_session"] = unauth_session.to_json()
    template = loader.get_template("crapdb/index.html")
    return HttpResponse(template.render(context, request))

def logout(request, session_id):
    unauth_session = get_unauth_session(request)

    try:
        # Update the unauth session with the hacker bucks and flags
        session = Session.get_session(session_id)
        unauth_session.from_other_session(session)
    except KeyError:
        pass

    AuthenticatedSession.logout(session_id)
    return redirect("crapdb:index")

def forgetful(request):
    context = {
        "unauth_session": get_unauth_session(request).to_json(),
        "forgetful_page_source": FLAGS["forgetful_page_source"][0],
        "valid_sec_answer": FLAGS["valid_sec_answer"][0]
    }
    template = loader.get_template('crapdb/forgetful.html')
    return HttpResponse(template.render(context, request))

def getpassword(request):
    context = {
        "unauth_session": get_unauth_session(request).to_json(),
        "forgetful_page_source": FLAGS["forgetful_page_source"][0],
        "valid_sec_answer": FLAGS["valid_sec_answer"][0]
    }

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        username = d.get("username", None)
        answer = d.get("answer", None)

        if username is None or answer is None:
            context["error"] = "You must provide an answer"
        elif not is_user_data_valid(username) or not is_user_data_valid(answer):
            context["error"] = "Too much data"
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
    context = {
        "unauth_session": get_unauth_session(request).to_json(),
        "forgetful_page_source": FLAGS["forgetful_page_source"][0],
        "valid_sec_answer": FLAGS["valid_sec_answer"][0]
    }

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        username = d.get("username", None)

        if username is not None:
            if not is_user_data_valid(username):
                context["error"] = "Too much data"
            else:
                query = "SELECT username, paid, question FROM users WHERE username='" + username + "' COLLATE NOCASE"
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

def querydb(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail

    ret = {"flags": []}

    if request.POST:
        conn = sqlite3.connect(settings.CRAPDB_PATH)
        cursor = conn.cursor()

        d = request.POST.dict()
        query = d.get("query", None)

        if query is not None:
            if not is_user_data_valid(query):
                ret["error"] = "Too much data"
            else:
                try:
                    ret["flags"] = [x for x in cursor.execute(query)]
                    if not ret["flags"]:
                        ret["error"] = "No flags found in database"
                except Exception as e:
                    ret["error"] = "'{}' - {}".format(query, str(e))

        conn.close()

    return HttpResponse(json.dumps(ret))

def checkflag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj # obj is session on success

    ret = {"hacker_bucks": session.hacker_bucks}

    if request.POST:
        d = request.POST.dict()
        flag = d.get("flag", None)

        if flag is not None:
            if not is_user_data_valid(flag, data_type=DataType.FLAG):
                ret["error"] = "Too much data"
            else:
                # Set's the session's hacker_bucks and prevents
                # getting points for the same flag more than once
                try:
                    update_hacker_bucks_from_flag(session, flag)
                    ret["hacker_bucks"] = session.hacker_bucks
                except FlagAlreadyClaimedError:
                    ret["error"] = "Already Claimed"

    return HttpResponse(json.dumps(ret))

def challenge_get(session, challenge_id):
    challenge = session.get_challenge(challenge_id)
    if challenge is None:
        raise KeyError("No challenge found with id: {}".format(challenge_id))

    # Raises exception NotEnoughHackerBucksError on fail
    session.hacker_bucks = challenge.purchase(session.hacker_bucks)
    return challenge

def challenge_get_flag(session, challenge_id, answer=""):
    ret = {"success": False}
    challenge = session.get_challenge(challenge_id)
    if challenge is None:
        raise KeyError("No challenge found with ID: {}".format(challenge_id))

    if not challenge.purchased:
        ret["error"] = "{} has not been purchased yet".format(challenge.meta.name)
        return ret

    if not is_user_data_valid(answer):
        ret["error"] = "Too much data"
        return ret

    res = challenge.check(answer)
    if res:
        ret["success"] = True
        try:
            flag = challenge.get_flag()
            ret["flag"] = flag
        except ChallengeNotSolvedError:
            pass # Answer was right but challenge isn't solved yet
    else:
        ret["error"] = "Invalid challenge answer"

    # Throw the challenge JSON on there for good measure
    ret.update(challenge.to_json())
    return ret

def super_admin_challenge_get_flag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj
    return HttpResponse(json.dumps(challenge_get_flag(session, "super_admin")))

def brutal_force_challenge_get(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj # object is session on success

    challenge = None
    try:
        challenge = challenge_get(session, "brutal_force")
    except NotEnoughHackerBucksError as e:
        return HttpResponse(json.dumps({"error": str(e)}))
    except KeyError as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    ret = {
        "hacker_bucks": session.hacker_bucks
    }
    ret.update(challenge.to_json())
    return HttpResponse(json.dumps(ret))

def brutal_force_challenge_get_flag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    ret = {}

    if request.POST:
        d = request.POST.dict()
        pin = d.get("pin", None)

        if pin is not None:
            if not is_user_data_valid(pin, data_type=DataType.PIN):
                ret["error"] = "The PIN should only be 4 digits"
            else:
                ret = challenge_get_flag(session, "brutal_force", answer=pin)
        else:
            ret["error"] = "No PIN provided in POST request"

    return HttpResponse(json.dumps(ret))

def rot_challenge_get(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    challenge = None
    try:
        challenge = challenge_get(session, "rot")
    except NotEnoughHackerBucksError as e:
        return HttpResponse(json.dumps({"error": str(e)}))
    except KeyError as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    ret = {
        "hacker_bucks": session.hacker_bucks
    }
    ret.update(challenge.to_json())
    return HttpResponse(json.dumps(ret))

def rot_challenge_get_flag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    ret = {}

    if request.POST:
        d = request.POST.dict()
        answer = d.get("answer", None)

        if answer is not None:
            if not is_user_data_valid(answer):
                ret["error"] = "Too much data"
            else:
                ret = challenge_get_flag(session, "rot", answer=answer)
        else:
            ret = {"error": "No answer provided in POST request"}

    return HttpResponse(json.dumps(ret))

def paid_content_challenge_get(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    challenge = None
    try:
        challenge = challenge_get(session, "paid_content")
    except NotEnoughHackerBucksError as e:
        return HttpResponse(json.dumps({"error": str(e)}))
    except KeyError as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    ret = {
        "hacker_bucks": session.hacker_bucks
    }
    ret.update(challenge.to_json())
    return HttpResponse(json.dumps(ret))

def paid_content_challenge_get_flag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    ret = challenge_get_flag(session, "paid_content", answer=session)
    return HttpResponse(json.dumps(ret))

def xor_challenge_get(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    challenge = None
    try:
        challenge = challenge_get(session, "xor")
    except NotEnoughHackerBucksError as e:
        return HttpResponse(json.dumps({"error": str(e)}))
    except KeyError as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    ret = {
        "hacker_bucks": session.hacker_bucks
    }
    ret.update(challenge.to_json())
    return HttpResponse(json.dumps(ret))

def xor_challenge_get_flag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    ret = {}

    if request.POST:
        d = request.POST.dict()
        answer = d.get("answer", None)

        if answer is not None:
            if not is_user_data_valid(answer, data_type=DataType.USER_SPECIFIED_EXACT_LENGTH, length=6):
                ret["error"] = "Passphrase must be 6 characters"
            else:
                ret = challenge_get_flag(session, "xor", answer=answer)
        else:
            ret = {"error": "No answer provided in POST request"}

    return HttpResponse(json.dumps(ret))

def genetic_challenge_get(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    challenge = None
    try:
        challenge = challenge_get(session, "genetic")
    except NotEnoughHackerBucksError as e:
        return HttpResponse(json.dumps({"error": str(e)}))
    except KeyError as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    ret = {
        "hacker_bucks": session.hacker_bucks
    }
    ret.update(challenge.to_json())
    return HttpResponse(json.dumps(ret))

def genetic_challenge_get_flag(request, session_id):
    status, obj = get_session(session_id, http_response=True)
    if not status:
        return obj # HttpResponse containing error on fail
    session = obj

    ret = {}

    if request.POST:
        d = request.POST.dict()
        answer = d.get("answer", None)

        if answer is not None:
            if not is_user_data_valid(answer, data_type=DataType.USER_SPECIFIED_EXACT_LENGTH, length=7):
                ret["error"] = "Password must be 7 characters"
            else:
                ret = challenge_get_flag(session, "genetic", answer=answer)
        else:
            ret = {"error": "No answer provided in POST request"}

    return HttpResponse(json.dumps(ret))
