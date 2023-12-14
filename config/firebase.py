from pathlib import Path
import os
import environ
import firebase_admin
from firebase_admin import credentials
from django.templatetags.static import static

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


cred = credentials.Certificate(static("/serviceAccountKey.json"))
firebase_app = firebase_admin.initialize_app(cred)
