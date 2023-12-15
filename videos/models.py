from django.db import models
from django.conf import settings
from common.models import CommonModel


# Create your models here.
class Video(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    video_file = models.FileField()


class Monitor(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
