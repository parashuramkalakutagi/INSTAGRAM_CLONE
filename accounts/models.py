from django.db import models
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
import uuid
from django.utils import timezone
import datetime
# Create your models here

class MySystemUserManager(BaseUserManager):


    def create_user(self, email, password=None):

        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user




class Profile(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    email = models.EmailField(verbose_name="Email", unique=True)
    username = models.CharField(blank=True, null=True, max_length=30)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    mobile_otp = models.CharField(max_length=10,default=0)
    mobile_otp_expired = models.IntegerField(default=0)
    email_otp = models.CharField(max_length=10,default=0)
    email_otp_expired = models.IntegerField(default=0)
    mobile_number = PhoneNumberField(unique=True, blank=True, default=None, null=True)
    mobile_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    bio = models.CharField(max_length=200,default=False,null=True,blank=True)
    profile_photo = models.ImageField(upload_to='Profile-images', null=True, blank=True)



    objects = MySystemUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def email_user(self, *args, **kwargs):
        send_mail(
            '{}'.format(args[0]),
            '{}'.format(args[1]),
            None,
            [self.email],
            fail_silently=False,
        )