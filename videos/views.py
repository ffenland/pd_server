import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.conf import settings
from firebase_admin import auth


class VideoView(APIView):
    def get(self, request):
        return Response({"ok": True})

    def post(self, request):
        id_token = request.data.get("idToken")
        file = request.data.get("file")
        if file and id_token:
            decoded_token = auth.verify_id_token(id_token)
            print(decoded_token)
            uid = decoded_token["uid"]
            print(file)

        return Response({"ok": True})


class VideoUploadView(APIView):
    def get(self, request):
        print(auth)
        return Response({"ok": True})
