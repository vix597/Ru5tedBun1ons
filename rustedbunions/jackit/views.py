from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.template import loader

from core.session import Session

def index(request, session_id):
    context = {}
    session = None

    try:
        session = Session.get_session(session_id)
    except KeyError:
        return redirect(reverse("crapdb:index") + "?error={}".format(
            "No session or session expired"))

    # TODO: Finish this

    template = loader.get_template('jackit/index.html')
    return HttpResponse(template.render(context, request))
