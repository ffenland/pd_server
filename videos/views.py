import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.conf import settings


class VideoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        if "file" not in request.FILES:
            return Response({"error": "No file found"}, status=HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES["file"]
        file_name = uploaded_file.name

        # 파일을 저장할 경로 지정 (static/videos 폴더에 저장)
        file_path = os.path.join(settings.STATIC_ROOT, "videos", file_name)

        try:
            # 파일을 저장
            with open(file_path, "wb") as file_object:
                for chunk in uploaded_file.chunks():
                    file_object.write(chunk)

            return Response({"success": f"File {file_name} uploaded successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
