from django.http import HttpResponse
from django.template import loader

from core.views import get_session

#pylint: disable=E1101

def index(request, session_id):
    context = {}
    status, obj = get_session(
        session_id, error="Login failed. No session or session expired")
    if not status:
        return obj # On fail obj is a redirect
    session = obj # On success obj is the session

    context["session_id"] = session_id
    context["session"] = session.to_json()
    template = loader.get_template('jackit/index.html')
    return HttpResponse(template.render(context, request))
