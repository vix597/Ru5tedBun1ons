import json

from django.shortcuts import redirect, reverse
from django.http import HttpResponse

from .session import Session, UnauthenticatedSession
from .models import Flag

class FlagAlreadyClaimedError(Exception):
    pass

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
            pure_flag = flag.replace("flag{", '')
            pure_flag = pure_flag.replace("}", '')
            if userflag == pure_flag:
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
        else:
            raise FlagAlreadyClaimedError()

def get_session(session_id, fail_url="crapdb:index",
                error="No session or session expired",
                http_response=False):
    '''
    Returns a tuple of (status, session or redirect)
     - If status is True the second element is a session object
     - If status is False the second element is a django redirect
    '''

    if len(session_id) != 32:
        # WTF is this shit?!
        print("********get_session() - Session ID length - Somebody is messing around*********")
        if not http_response:
            return (False, redirect(reverse(fail_url) + "?error={}".format(error)))
        else:
            return (False, HttpResponse(json.dumps({"redirect": error})))

    session = None
    try:
        session = Session.get_session(session_id)
    except KeyError:
        if not http_response:
            return (False, redirect(reverse(fail_url) + "?error={}".format(error)))
        else:
            return (False, HttpResponse(json.dumps({"redirect": error})))

    return (True, session)

def get_unauth_session(request):
    unauth_session = None

    if "unauth_session" not in request.session:
        unauth_session = UnauthenticatedSession()
        request.session["unauth_session"] = unauth_session.oid
    else:
        session_id = request.session["unauth_session"]
        if len(session_id) != 32:
            # WTF is this shit?!
            print("********get_unauth_session() - Session ID length - Somebody is messing around*********")
            unauth_session = UnauthenticatedSession()
            request.session["unauth_session"] = unauth_session.oid
            return unauth_session

        try:
            unauth_session = Session.get_session(request.session["unauth_session"])
        except KeyError:
            unauth_session = UnauthenticatedSession(oid=request.session["unauth_session"])

    return unauth_session

def checkflag(request, session_id):
    try:
        session = Session.get_session(session_id)
    except KeyError:
        session = UnauthenticatedSession(oid=session_id)

    ret = {"hacker_bucks": session.hacker_bucks}

    if request.POST:
        d = request.POST.dict()
        flag = d.get("flag", None)

        if flag is not None:
            try:
                update_hacker_bucks_from_flag(session, flag)
                ret["hacker_bucks"] = session.hacker_bucks
            except FlagAlreadyClaimedError:
                ret["error"] = "Already claimed"

    return HttpResponse(json.dumps(ret))
