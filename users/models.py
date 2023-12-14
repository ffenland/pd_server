from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    # Veil Useless field
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # 유저는 하나의 유니크한 keycode를 갖는다.
    # 키코드는 숫자로 구성된 8자리 문자열.
    key_code = models.CharField(
        max_length=8,
    )
