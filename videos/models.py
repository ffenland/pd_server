from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from common.models import CommonModel


# Create your models here.
class Video(CommonModel):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Monitor(CommonModel):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
