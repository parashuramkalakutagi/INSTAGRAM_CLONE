from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.status import *
from django.db.models import Sum,Count,Max,Min,Q,F
from accounts.models import Profile

class PostView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request,*args,**kwargs):
        queryset = Posts.objects.filter(Q(user_id=request.user) and Q(Profile_id__user= request.user)).values('uuid','post','created_at')
        return Response(queryset)

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user = request.user

            Posts.objects.create(
                Profile_id=Profile_Page.objects.get(uuid=data.get('Profile_id')),
                user_id=Profile.objects.get(email=user),
                post=data.get('post')
            )
            return Response({'msg': 'Post Uploded', 'Code': 201}, status=HTTP_201_CREATED)

        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)

class VideoPostView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self,request,*args,**kwargs):
        queryset = VideoPost.objects.filter(Q(user_id=request.user) and Q(Profile_id__user=request.user)).values('uuid','file','created_at')
        return Response(queryset)
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user = request.user

            VideoPost.objects.create(
                Profile_id=Profile_Page.objects.get(uuid=data.get('Profile_id')),
                user_id=Profile.objects.get(email=user),
                file=data['file']
            )
            return Response({'msg': 'Video Uploaded..', 'Code': 201}, status=HTTP_201_CREATED)

        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)




class HighlightsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self,request,*args,**kwargs):
        queryset = hightlites.objects.filter(Q(user_id=request.user) and Q(Profile_id__user_id=request.user)).values_list('stories',flat=True)
        return Response(queryset)


    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user = request.user

            hightlites.objects.create(
                Profile_id=Profile_Page.objects.get(uuid=data.get('Profile_id')),
                user_id=Profile.objects.get(email=user),
                stories=data['stories']
            )
            return Response({'msg': 'Highlights Uploaded..', 'Code': 201}, status=HTTP_201_CREATED)

        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class LikeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self,request,*args,**kwargs):
        queryset = Likes.objects.filter(Q(user_id=request.user) and Q(profile_id__user=request.user)).aggregate(total_likes = Count('post_id__likes__profile_id'))
        return Response(queryset)

    def create(self, request, *args, **kwargs):

            data = request.data
            user_id = request.user
            if Likes.objects.filter(user_id=user_id,
                                    profile_id=data.get('profile_id'),
                                    post_id=data.get('post_id')).exists():
                return Response({'msg': 'alredy this user is liked post'}, status=HTTP_400_BAD_REQUEST)

            Likes.objects.create(user_id=Profile.objects.get(email=user_id),
                                 profile_id=Profile_Page.objects.get(uuid=data.get('profile_id')),
                                 post_id=Posts.objects.get(uuid=data.get('post_id')))

            return Response({'msg': ' post is liked'})

    def delete(self,request,*args,**kwargs):
        data = request.data
        user = request.user

        unlike  = Likes.objects.filter(post_id=data['post_id'],user_id=user)
        if not unlike.exists():
            return Response({'msg':'Alredy Unliked Post  ','code':400},status=HTTP_400_BAD_REQUEST)

        unlike[0].delete()
        return Response({'msg':'Post Unliked ','code':200},status=HTTP_200_OK)

class StoriesView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            user_id  = request.user
            Stories.objects.create(user_id = Profile.objects.get(email= user_id),
                                   Profile_id = Profile_Page.objects.get(uuid = request.data.get('Profile_id')),
                                   file = data.get('file'),
                                   expiridate = datetime.datetime.now() + datetime.timedelta(minutes=5),
                                   ),

            return Response({'data':{'msg':'story uploded...'}},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error':e},status=HTTP_400_BAD_REQUEST)


# class CommentsCountView(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def list(self, request, *args, **kwargs):
#      queryset = Comments.objects.all().values('post_id__comments__user_id__email').annotate(total_comments = Count('post_id__comments__user_id__email'))
#      return Response(queryset)

class CommentsViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request,*args,**kwargs):
        queryset = Comments.objects.all()
        serializer = CommentsSerializer(queryset,many=True).data
        return Response(serializer)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user_id = request.user

            Comments.objects.create(user_id=Profile.objects.get(email = user_id),
                                    post_id = Posts.objects.get(uuid = data.get('post_id')),
                                    message = data.get('message'))
            return Response({'msg':'comment is posted '},status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg':'something went wrong'},status=HTTP_400_BAD_REQUEST)


class FollowingViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            if Following.objects.filter(
                user_id=request.user,
                following_id = data.get('following_id'),
            ).exists():
                return Response({'msg':'Alredy Following '},status=HTTP_400_BAD_REQUEST)

            Following.objects.create(user_id=request.user,
                                     following_id=Profile_Page.objects.get(uuid=request.data.get('following_id')))
            return Response({'msg': 'following ...!'}, status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'msg': '400  bad request'}, status=HTTP_400_BAD_REQUEST)




