import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_application.settings")
setup()
