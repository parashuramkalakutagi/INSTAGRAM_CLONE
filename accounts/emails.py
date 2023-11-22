import random
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from .models import *


def send_via_mail(email):
    subject = f' FORGOT PASSWORD '
    otp = random.randint(1000,9999)
    message = f'password reset  otp is {otp} '
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj = Profile.objects.get(email= email)
    user_obj.mobile_otp = otp
    user_obj.save()
    return otp

def send_story_deleted_mail(email,username):
    subject = f'mr.{username} Your story is expired '
    message = 'now it will be deleted \n now you can post anthor story'
    email_from = settings.EMAIL_HOST
    send_mail(subject=subject,message=message,from_email=email_from,recipient_list=[email])
