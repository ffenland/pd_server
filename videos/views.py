import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.conf import settings
from firebase_admin import auth, db
from .models import Video


def writeFirebaseDB(key_code, file_name, file_path):
    # firebase Database

    ref = db.reference(f"files/{key_code}/{file_name.split('.')[0]}")
    ref.set(
        {
            "path": f"{file_path}/{file_name}",
            "state": "pause",
        }
    )


class VideoView(APIView):
    def get(self, request):
        return Response({"ok": True})


class VideoUploadView(APIView):
    def get(self, request):
        print(auth)
        return Response({"ok": True})

    def post(self, request):
        file = request.data.get("file")
        if file and request.user:
            try:
                user = request.user
                upload_path = os.path.join("static", "videos", f"{user.key_code}")
                os.makedirs(upload_path, exist_ok=True)
                # 중복 파일명 체크
                file_name = file.name
                file_path = os.path.join(upload_path, file_name)
                count = 1
                while os.path.exists(file_path):
                    # 중복되는 경우 숫자를 추가하여 파일 이름 변경
                    file_name = f"{os.path.splitext(file.name)[0]}_{count}{os.path.splitext(file.name)[1]}"
                    file_path = os.path.join(upload_path, file_name)
                    count += 1

                # 파일 저장
                with open(os.path.join(upload_path, file_name), "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                Video.objects.create(
                    user=request.user,
                    title=file_name,
                    video_file=f"static/videos/{user.key_code}/{file.name}",
                )
                # firebase Database

                writeFirebaseDB(
                    key_code=user.key_code,
                    file_name=file_name,
                    file_path=upload_path,
                )

                return Response({"ok": True})
            except Exception:
                return Response({"ok": False})

        else:
            return Response({"ok": False})
