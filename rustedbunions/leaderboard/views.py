import json
import hashlib
from html.parser import HTMLParser

from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

from flags import FLAGS
from core.util import is_user_data_valid, DataType
from core.views import get_unauth_session, calc_lifetime_hacker_bucks_from_claimed_flags
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
        "leaderboard": get_leaderboard(),
        "num_flags": len(FLAGS)
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
            if not is_user_data_valid(name, data_type=DataType.SHORT_NAME):
                ret["error"] = "Too much data"
            elif not is_user_data_valid(secret_key, data_type=DataType.PASSWORD):
                ret["error"] = "Too much data"
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

                    leader_purchased_challenges = json.loads(leader.purchased_challenges)
                    for challenge_id in leader_purchased_challenges:
                        challenge = session.get_challenge(challenge_id)
                        if challenge:
                            challenge.purchased = True
                else:
                    ret["error"] = "Cannot find leader with the provided name/secret_key combination"
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
            if not is_user_data_valid(name, data_type=DataType.SHORT_NAME):
                ret["error"] = "Too much data"
            elif not is_user_data_valid(secret_key, data_type=DataType.PASSWORD):
                ret["error"] = "Too much data"
            elif get_leader(name.strip().lower()):
                # If they also proved the correct secret key, update that entry in the database
                secret_key = hashlib.sha512(secret_key.encode('utf-8')).hexdigest()
                leader = get_leader(name.strip().lower(), secret_key)
                if leader:
                    session = get_unauth_session(request)
                    if not session.lifetime_hacker_bucks:
                        ret["error"] = "What makes you think you belong on the leaderboard?"
                    else:
                        # Update the leader with the new info
                        # Create a set of claimed flags and combine the loaded leader with the current session
                        leader_claimed_flags = json.loads(leader.claimed_flags)
                        claimed_flags = list(set(leader_claimed_flags + session.claimed_flags))

                        leader.lifetime_hacker_bucks = calc_lifetime_hacker_bucks_from_claimed_flags(claimed_flags)
                        leader.num_flags_found = len(claimed_flags)
                        leader.claimed_flags = json.dumps(claimed_flags)
            
                        # This will overwrite their hacker bucks. Only an issue if they didn't load first
                        leader.hacker_bucks = session.hacker_bucks
                        leader.remote_ip = session.remote_ip
                        leader.percent_complete = int((leader.num_flags_found) / len(FLAGS) * 100)
                        leader.playtime = str(timezone.now() - leader.session_creation_time)

                        leader_purchased_challenges = json.loads(leader.purchased_challenges)
                        for challenge_id, challenge in session.challenges.items():
                            if challenge.purchased:
                                leader_purchased_challenges.append(challenge_id)
                        leader_purchased_challenges = list(set(leader_purchased_challenges))
                        leader.purchased_challenges = json.dumps(leader_purchased_challenges)

                        # Update the changes
                        leader.save()
                else:
                    ret["error"] = "Already a leader with that name. To update, provide the correct password."
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
                    leader.remote_ip = session.remote_ip
                    leader.session_creation_time = session.creation_time
                    leader.secret_key = hashlib.sha512(secret_key.encode('utf-8')).hexdigest()
                    leader.playtime = str(timezone.now() - session.creation_time)

                    # Get the list of purchased challenge IDs
                    purchased_challenges = []
                    for challenge_id, challenge in session.challenges.items():
                        if challenge.purchased:
                            purchased_challenges.append(challenge_id)
                    leader.purchased_challenges = json.dumps(purchased_challenges)

                    leader.save()
        else:
            ret["error"] = "No name/secret key provided for leaderboard entry"

        if "error" not in ret:
            parser = HTMLParser()
            parser.feed(name)
            parser.close()
            if parser.get_starttag_text():
                ret["flag"] = FLAGS["scoreboard_hacking"][0]

    return HttpResponse(json.dumps(ret))
