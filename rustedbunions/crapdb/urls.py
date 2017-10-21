from django.conf.urls import url
from . import views

app_name = "crapdb"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'login/$', views.login, name="login"),
    url(r'forgetful/$', views.forgetful, name="forgetful"),
    url(r'searchcrap/$', views.searchcrap, name="searchcrap"),
    url(r'main/(?P<session_id>\w+)/$', views.main, name="main"),
    url(r'logout/(?P<session_id>\w+)/$', views.logout, name="logout"),
]
