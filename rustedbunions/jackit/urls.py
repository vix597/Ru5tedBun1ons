from django.conf.urls import url
from . import views

app_name = "jackit"
urlpatterns = [
    url(r'(?P<session_id>\w+)/$', views.index, name="index"),
]
