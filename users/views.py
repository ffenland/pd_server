import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.conf import settings
from firebase_admin import auth, db


# Create your views here.
class Me(APIView):
    def get(self, request):
        user = request.user
        me = {
            "uid": user.username,
            "key_code": user.key_code,
        }
        return Response({"ok": True, "user": me})
