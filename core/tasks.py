from celery import shared_task
from datetime import timedelta
# from datetime import timezone
from .models import Stories
from instagram import settings
from django.utils import timezone


@shared_task(bind= True)
def delete_old_story(self):
    storiess = Stories.objects.all()
    for story in storiess:
        if story.expiridate < timezone.localtime(timezone.now()):
            story.delete()
    return " story deleted"