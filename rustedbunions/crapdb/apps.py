from django.apps import AppConfig

#pylint: disable=W0401, W0614
from .challenges import *

class CrapdbConfig(AppConfig):
    name = 'crapdb'
