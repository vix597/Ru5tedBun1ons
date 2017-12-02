import json
from datetime import datetime

from django.http import HttpResponse
from django.template import loader
from flags import FLAGS

from core.views import get_unauth_session
from .models import LeaderboardEntry

def get_leaderboard():
    '''
    Get all the entries in the leaderboard
    '''
    try:
        #pylint: disable=E1101
        ret = LeaderboardEntry.objects.order_by("-lifetime_hacker_bucks", "playtime", "-flags_found")
        if len(ret) > 50:
            ret = ret[:50]
        return ret
    except:
        return []

def index(request):
    context = {
        "unauth_session": get_unauth_session(request).to_json(),
        "leaderboard": get_leaderboard()
    }
    template = loader.get_template('leaderboard/index.html')
    return HttpResponse(template.render(context, request))

def submit(request):
    ret = {}

    if request.POST:
        d = request.POST.dict()
        name = d.get("name", None)

        if name:
            session = get_unauth_session(request)
            if not session.lifetime_hacker_bucks:
                ret["error"] = "What makes you think you belong on the leaderboard?"
            else:
                leader = LeaderboardEntry()
                leader.lifetime_hacker_bucks = session.lifetime_hacker_bucks
                leader.flags_found = len(session.claimed_flags)
                leader.hacker_bucks = session.hacker_bucks
                leader.percent_complete = int((leader.flags_found / len(FLAGS)) * 100)
                leader.name = name
                leader.playtime = str(datetime.utcnow() - session.creation_time)
                leader.save()
        else:
            ret["error"] = "No name provided for leaderboard entry"

    return HttpResponse(json.dumps(ret))
