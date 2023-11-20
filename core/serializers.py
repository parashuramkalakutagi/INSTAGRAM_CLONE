from rest_framework import serializers
from .models import Comments,Profile,Profile_Page,Posts,VideoPost
from django.db.models import Q,F,Count,aggregates,Aggregate
from rest_framework import request

class ProfilePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile_Page
        fields = ['uuid','name']

class PostSerializer(serializers.ModelSerializer):
    # Profile_id = ProfilePageSerializer(many=False)
    total_posts = serializers.SerializerMethodField('get_all_post_count')
    class Meta:
        model = Posts
        fields = ['uuid','Profile_id','post','total_posts']

    def get_all_post_count(self,obj):
        if obj:
            queryset = Posts.objects.all().count()
            return queryset
        else:
            return None


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','user_name','email',]


class CommentsSerializer(serializers.ModelSerializer):
    post_id = PostSerializer(many=False)
    # post_id = serializers.SerializerMethodField('get_post')
    # user_id = serializers.SerializerMethodField('get_user')
    user_id = ProfileSerializer(many=False)
    total_comments = serializers.SerializerMethodField('get_total_comments')
    all_count = serializers.SerializerMethodField('get_all_count')
    class Meta:
        model = Comments
        fields = ['post_id','user_id','message','all_count','total_comments']

    def get_total_comments(self,obj):
        if obj:
            queryset = Comments.objects.filter(post_id=obj.post_id).values_list('message',flat=True)
            return queryset
        else:
            return None

    def get_all_count(self,obj):
        if obj:
            queryset = Comments.objects.filter(post_id=obj.post_id).aggregate(comments_count = Count('message'))
            return queryset
        else:
            return None