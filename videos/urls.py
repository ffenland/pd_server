from django.urls import path
import views

urlpatterns = [
    path("upload/", views.VideoUploadView.as_view()),
]
