from django.db import models
import uuid
from accounts.models import Profile
from datetime import timedelta
from django.utils import timezone
import datetime

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract  = True

class Profile_Page(BaseModel):
    user = models.OneToOneField(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=250,null=True,blank=True)
    slug = models.URLField(max_length=200,null=True,blank=True)
    gender = models.CharField(max_length=20, choices=(("m", "Male"), ("F", "Female")))
    profile_photo = models.ImageField(upload_to='Profile-images', null=True, blank=True)

    def __str__(self):
        return f'{str(self.name)} =======  {str(self.uuid)}'


class Posts(BaseModel):
    user_id  = models.ForeignKey(Profile,on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    post = models.ImageField(upload_to='posts')

    def __int__(self):
        return self.user_id



class VideoPost(BaseModel):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    file = models.FileField(upload_to='POST_VIDEOS')

    def __str__(self):
        return self.user_id

class hightlites(BaseModel):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    stories = models.FileField(upload_to='STORIES')

class Likes(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile_Page, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} is liked this post >>  {self.post_id}'

class Followers(models.Model):
    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    followers_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE,related_name='followers_id')

    def __str__(self):
        return f'{self.user_id} is following {self.followers_id}'

class Following(models.Model):
    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    following_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE,related_name='following',related_query_name='following')

class Comments(models.Model):
    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    message = models.CharField(max_length=150)


class Stories(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Profile_id = models.ForeignKey(Profile_Page,on_delete=models.CASCADE)
    file = models.FileField(upload_to='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    expiridate = models.DateTimeField()


