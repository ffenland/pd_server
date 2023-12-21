import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.conf import settings
from firebase_admin import auth, db
from .models import Video

base_url = "http://boripharma.ipdisk.co.kr:9875/"
static_path = "static/videos/"


def writeFirebaseDB(key_code, file_name):
    # firebase Database

    ref = db.reference(f"files/{key_code}/{file_name.split('.')[0]}")
    ref.set(
        {
            "path": f"{base_url + static_path}{key_code}/{file_name}",
            "state": "pause",
        }
    )


def deleteFirebaseDB(key_code, file_name):
    ref = db.reference(f"files/{key_code}/{file_name.split('.')[0]}")
    ref.delete()


def delete_file(key_code, file_name):
    file_path = os.path.join("static", "videos", key_code, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_monitor_file(key_code, file_path):
    ref = db.reference(f"monitors/{key_code}")
    monitors = ref.get()
    if monitors:
        for monitor_key, monitor_value in monitors.items():
            if ("files") in monitor_value:
                files = monitor_value["files"]
                if file_path in files:
                    print(files)
                    files.remove(file_path)
                    ref.child(f"{monitor_key}/files").set(files)


class VideoView(APIView):
    def get(self, request):
        key_code = request.data.get("key_code")
        print(key_code)
        # Show user's all videos.
        # firebase
        ref = db.reference(f"files/{key_code}")
        snapshot = ref.order_by_key().get()
        if snapshot:
            for key, val in snapshot.items():
                if isinstance(val.get("path"), str):  # 'path' 키의 값이 문자열인 경우에만 처리
                    val["path"] = val["path"].replace("\\", "/")  # 문자열에서 역슬래시를 슬래시로 변경
                state = val.get("state")
                path = val.get("path")
                print(f"{key} is {state}, {path}")
            return Response({"ok": True})
        else:
            return Response({"ok": False})

    def post(self, request):
        # handle uploaded video file.
        file = request.data.get("file")
        key_code = request.data.get("key_code")
        if file and request.user and key_code:
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

                # firebase Database

                writeFirebaseDB(
                    key_code=key_code,
                    file_name=file_name,
                )

                return Response({"ok": True})
            except Exception:
                return Response({"ok": False})

        else:
            return Response({"ok": False})

    def put(self, request):
        file_path = request.data.get("filePath")
        key_code = request.user.key_code
        file_name = file_path.split("/")[-1]

        try:
            delete_file(key_code, file_name)
            deleteFirebaseDB(key_code, file_name)
            delete_monitor_file(key_code, file_path)

            return Response({"ok": True})

        except Exception as e:
            return Response({"ok": False, "error": str(e)})
