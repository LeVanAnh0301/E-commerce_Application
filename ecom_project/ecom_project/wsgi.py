"""
WSGI config for ecom_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
application = get_wsgi_application()
project_folder = os.path.expanduser('~/ecom_project')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

