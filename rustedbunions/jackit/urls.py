from django.conf.urls import url
from . import views

app_name = "jackit"
urlpatterns = [
    url(r'^$', views.index, name="index"),
]
