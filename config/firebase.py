import os
import firebase_admin
import random
import string


from pathlib import Path
from firebase_admin import auth as firebase_auth
from firebase_admin import db as firebase_db
from firebase_admin import credentials
from rest_framework import authentication, exceptions
from users.models import User
from django.utils import timezone

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
if not firebase_admin._apps:
    firebase_app = firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://p-app-service-default-rtdb.asia-southeast1.firebasedatabase.app/"
        },
    )


# def generate_unique_key():
#     length = 8
#     while True:
#         key_code = "".join(random.choices(string.digits, k=length))
#         if not User.objects.filter(key_code=key_code).exists():
#             return key_code


def get_key_code(user_uid):
    pass


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise exceptions.AuthenticationFailed("No auth token provided")
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid auth token")

        if not id_token or not decoded_token:
            return None
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise firebase_auth.UserNotFoundError

        user, created = User.objects.get_or_create(
            username=uid,
        )

        if created:
            ref = firebase_db.reference(f"keyCode/{uid}")
            new_key_code = ref.get()
            user.key_code = new_key_code
            user.save()
        return (user, None)
