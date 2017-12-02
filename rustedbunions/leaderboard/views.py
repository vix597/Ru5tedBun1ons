import json
import hashlib
from datetime import datetime

from django.http import HttpResponse
from django.template import loader
from flags import FLAGS

from core.util import ObjectId
from core.views import get_unauth_session
from .models import LeaderboardEntry

def get_leaderboard():
    '''
    Get all the entries in the leaderboard
    '''
    try:
        #pylint: disable=E1101
        ret = LeaderboardEntry.objects.order_by("-lifetime_hacker_bucks", "playtime", "-num_flags_found")
        if len(ret) > 50:
            ret = ret[:50]
        return ret
    except:
        return []

def get_leader(name, secret_key=None):
    '''
    Get a specific leader entry to load
    '''
    try:
        #pylint: disable=E1101
        if secret_key:
            ret = LeaderboardEntry.objects.filter(name=name, secret_key=secret_key)
        else:
            ret = LeaderboardEntry.objects.filter(name=name)
        if len(ret) == 1:
            ret = ret[0]
        return ret
    except:
        return None

def index(request):
    context = {
        "unauth_session": get_unauth_session(request).to_json(),
        "leaderboard": get_leaderboard()
    }
    template = loader.get_template('leaderboard/index.html')
    return HttpResponse(template.render(context, request))

def load(request):
    ret = {}

    if request.POST:
        d = request.POST.dict()
        name = d.get("name", None)
        secret_key = d.get("secret_key", None)

        if name and secret_key:
            if len(name) > 25:
                ret["error"] = "Name cannot be longer than 25 characters"
            elif len(secret_key) > 128:
                ret["error"] = "I have to hash that password you know! 128 characters max. Thanks."
            else:
                name = name.strip().lower() # Normalize the name
                session = get_unauth_session(request)
                secret_key = hashlib.sha512(secret_key.encode('utf-8')).hexdigest()
                leader = get_leader(name, secret_key)
                if leader:
                    session.lifetime_hacker_bucks = leader.lifetime_hacker_bucks
                    session.claimed_flags = json.loads(leader.claimed_flags)
                    session.hacker_bucks = leader.hacker_bucks
                    session.creation_time = leader.session_creation_time
                else:
                    ret["error"] = "Cannot find leader with the provided name/secret_key/OID combination"
        else:
            ret["error"] = "Invalid POST request. Missing cirtical information"

    return HttpResponse(json.dumps(ret))

def submit(request):
    ret = {}

    if request.POST:
        d = request.POST.dict()
        name = d.get("name", None)
        secret_key = d.get("secret_key", None)

        if name and secret_key:
            if len(name) > 25:
                ret["error"] = "Name cannot be longer than 25 characters"
            elif len(secret_key) > 128:
                ret["error"] = "I have to hash that password you know! 128 characters max. Thanks."
            elif get_leader(name.strip().lower()):
                ret["error"] = "There's already a leader with that name"
            else:
                name = name.strip()
                session = get_unauth_session(request)
                if not session.lifetime_hacker_bucks:
                    ret["error"] = "What makes you think you belong on the leaderboard?"
                else:
                    leader = LeaderboardEntry()
                    leader.lifetime_hacker_bucks = session.lifetime_hacker_bucks
                    leader.num_flags_found = len(session.claimed_flags)
                    leader.claimed_flags = json.dumps(session.claimed_flags)
                    leader.hacker_bucks = session.hacker_bucks
                    leader.percent_complete = int((leader.num_flags_found / len(FLAGS)) * 100)
                    leader.name = name.lower()
                    leader.display_name = name
                    leader.session_creation_time = session.creation_time
                    leader.secret_key = hashlib.sha512(secret_key.encode('utf-8')).hexdigest()
                    leader.playtime = str(datetime.utcnow() - session.creation_time)
                    leader.save()
        else:
            ret["error"] = "No name/secret key provided for leaderboard entry"

    return HttpResponse(json.dumps(ret))
