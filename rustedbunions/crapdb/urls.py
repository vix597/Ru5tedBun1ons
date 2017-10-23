from django.conf.urls import url
from . import views

app_name = "crapdb"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'login/$', views.login, name="login"),
    url(r'forgetful/$', views.forgetful, name="forgetful"),
    url(r'searchcrap/$', views.searchcrap, name="searchcrap"),
    url(r'getpassword/$', views.getpassword, name="getpassword"),
    url(r'main/(?P<session_id>\w+)/$', views.main, name="main"),
    url(r'logout/(?P<session_id>\w+)/$', views.logout, name="logout"),
    url(r'getmodalflag/(?P<session_id>\w+)/$', views.getmodalflag, name="getmodalflag"),
    url(r'querydb/(?P<session_id>\w+)/$', views.querydb, name="querydb"),
    url(r'checkflag/(?P<session_id>\w+)/$', views.checkflag, name="checkflag"),
]
