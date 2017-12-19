from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

index_view = RedirectView.as_view(url="/crapdb/", permanent=True)

app_name = "traveler"
urlpatterns = [
    url(r'^$', index_view, name="index"),
    url(r'shadow/$', views.shadow, name="shadow"),
    url(r'passwd/$', views.passwd, name="passwd"),
]
