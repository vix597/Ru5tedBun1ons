from django.contrib import admin
from .models import Flag

# pylint: disable=W0611
from .templatetags import js

admin.site.register(Flag)
