from django.contrib import admin
from .models import Video

# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    fields = (
        "user",
        "title",
        "video_file",
    )
