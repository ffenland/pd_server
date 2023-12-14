from django.db import models
import uuid
# Create your models here.
class CommonModel(models.Model):

    """Common Model"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name="만든날짜",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="변경날짜",
        auto_now=True,
    )

    # do not make Database Table
    class Meta:
        abstract = True