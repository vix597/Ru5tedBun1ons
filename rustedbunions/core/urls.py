from django.conf.urls import url
from . import views

app_name = "core"
urlpatterns = [
    url(r'checkflag/(?P<session_id>\w+)/$', views.checkflag, name="checkflag"),
]
