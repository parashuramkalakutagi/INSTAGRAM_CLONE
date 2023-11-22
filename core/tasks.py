from celery import shared_task
from datetime import timedelta
# from datetime import timezone
from .models import Stories
from instagram import settings
from accounts.models import Profile
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.status import *
from accounts.emails import send_story_deleted_mail



@shared_task(bind= True)
def delete_old_story(self):
    storiess = Stories.objects.all()
    for story in storiess:
        if story.expiridate < timezone.localtime(timezone.now()):
            story.delete()
            obj = story.user_id.email
            username = story.Profile_id.name
            send_story_deleted_mail(obj,username)
    return " story deleted"