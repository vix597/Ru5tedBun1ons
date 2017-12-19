from django.conf.urls import url
from . import views

app_name = "crapdb"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'shadow/$', views.shadow, name="shadow"),
    url(r'passwd/$', views.passwd, name="passwd"),
    url(r'about/$', views.about, name="about"),
    url(r'login/$', views.login, name="login"),
    url(r'forgetful/$', views.forgetful, name="forgetful"),
    url(r'searchcrap/$', views.searchcrap, name="searchcrap"),
    url(r'getpassword/$', views.getpassword, name="getpassword"),
    url(r'main/(?P<session_id>\w+)/$', views.main, name="main"),
    url(r'logout/(?P<session_id>\w+)/$', views.logout, name="logout"),
    url(r'querydb/(?P<session_id>\w+)/$', views.querydb, name="querydb"),
    url(r'checkflag/(?P<session_id>\w+)/$', views.checkflag, name="checkflag"),
    url(r'superadmin/(?P<session_id>\w+)/$', views.super_admin_challenge_get_flag, name="superadmin"),
    url(r'brutalforce/(?P<session_id>\w+)/$', views.brutal_force_challenge_get, name="brutalforce"),
    url(r'brutalforceflag/(?P<session_id>\w+)/$', views.brutal_force_challenge_get_flag, name="brutalforceflag"),
    url(r'rot/(?P<session_id>\w+)/$', views.rot_challenge_get, name="rot"),
    url(r'rotflag/(?P<session_id>\w+)/$', views.rot_challenge_get_flag, name="rotflag"),
    url(r'paidcontent/(?P<session_id>\w+)/$', views.paid_content_challenge_get, name="paidcontent"),
    url(r'paidcontentflag/(?P<session_id>\w+)/$', views.paid_content_challenge_get_flag, name="paidcontentflag"),
    url(r'xor/(?P<session_id>\w+)/$', views.xor_challenge_get, name="xor"),
    url(r'xorflag/(?P<session_id>\w+)/$', views.xor_challenge_get_flag, name="xorflag"),
]
