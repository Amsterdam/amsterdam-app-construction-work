import os
from django import setup
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_application.testing_settings")
setup()

call_command('migrate')
