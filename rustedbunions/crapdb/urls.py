from django.conf.urls import url
from . import views

app_name = "crapdb"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'login/$', views.login, name="login"),
    url(r'forgetful/$', views.forgetful, name="forgetful"),
    url(r'searchcrap/$', views.searchcrap, name="searchcrap"),
]
