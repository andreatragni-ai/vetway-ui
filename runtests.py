"""Esegue i test del pacchetto senza un progetto ospite:
    python runtests.py
Da un ospite valgono anche: manage.py test vetway_ui
"""
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

settings.configure(
    DEBUG=False,
    INSTALLED_APPS=['django.contrib.staticfiles', 'vetway_ui'],
    STATIC_URL='/static/',
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'APP_DIRS': True}],
    SECRET_KEY='test',
)
django.setup()
sys.exit(bool(get_runner(settings)().run_tests(['vetway_ui'])))
