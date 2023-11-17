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
