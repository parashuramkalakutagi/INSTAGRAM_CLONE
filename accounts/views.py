from django.shortcuts import render
from .models import Profile
from .serializer import *
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,BlacklistedToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .emails import send_via_mail,Util
from .backend import RegisterAuthBackend
import jwt
import time
from instagram import settings
import re
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from django.urls import reverse
from django.conf import settings
from .email_templates import EmailTokenTemplates


def validate_args(data, args):
    for key in args:
        if key not in data.keys():
            return Response({"message": f"Invalid Arguments, required {key}", "code": 400}, status=HTTP_400_BAD_REQUEST)

    return False

def validate_email_address(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False


class SingUpViewset(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        data = request.data
        validate = validate_args(data,['email','user_name','password'])
        auth = RegisterAuthBackend()

        if auth.email_verify(email=data['email']):
            return Response({'msg':'Email Is Alredy Exists...!'},status=HTTP_400_BAD_REQUEST)

        if validate:
            return validate
        object =  Profile.objects.create(
            email = data['email'],
            user_name=data['user_name'],
            email_verified= False,
        )
        object.set_password(data['password'])
        object.save()

        user = Profile.objects.filter(email= data['email']).first()
        token = jwt.encode({'email':user.email},key=settings.JWT_SECRET,algorithm='HS256')
        EmailTokenTemplates.verify_email(user,token)
        return Response({'msg':'Please Check email to Verification '},status=HTTP_201_CREATED)

    def patch(self,request,*args,**kwargs):
        data = request.data
        user = Profile.objects.get(email = data['email'])
        if user:
            user.profile_photo = data['profile_photo']
            user.bio = data['bio']
            user.save()
            return Response({'msg':'Profile is Updated'},status=HTTP_206_PARTIAL_CONTENT)
        else:
            return Response({'msg':'Invalid User email'},status=HTTP_400_BAD_REQUEST)


class Verify_Email(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        try:
            token = self.request.GET['token']
            token_decode = jwt.decode(token, key=settings.JWT_SECRET, algorithms='HS256')
            user = Profile.objects.get(email__exact=token_decode['email'])

            if not user.email_verified:
                user.email_verified = True
                user.save()
                return Response({"message": "Email verified successfully, Please login", "code": 200},
                                status=HTTP_200_OK)
            else:
                return Response({"message": "Invalid otp token", "code": 400}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            responce_data = {
                'msg':'erorr',
                'error':e,
                'status':HTTP_400_BAD_REQUEST
            }
            return Response(responce_data,status=HTTP_400_BAD_REQUEST)



class Delete_EmailUser(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        token = self.request.GET['token']
        decode = jwt.decode(token,key=settings.JWT_SECRET,algorithms='HS256')
        user = Profile.objects.get(email__exact=decode['email'])
        if user:
            user.delete()
            return Response({'msg':'User email deleted '},status=HTTP_200_OK)
        else:
            return Response({'msg':'User not found'},status=HTTP_400_BAD_REQUEST)



class LoginView(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            validate = validate_args(data, ['email', 'password'])
            if validate:
                return validate

            if not validate_email_address(data['email']):
                return Response({'msg': 'Invalid email'}, status=HTTP_400_BAD_REQUEST)

            user = Profile.objects.get(email__exact=data['email'])
            user.check_password(data['password'])

            if user:
                if user.is_admin:
                    if user.is_active:
                        if user.email_verified:
                            token = RefreshToken.for_user(user)
                            token = {
                                "access_token": str(token.access_token),
                                "refresh_token": str(token),
                                "is_admin": user.is_admin,
                                "message": "Login success",
                                "code": 200
                            }
                            return Response(token, status=HTTP_200_OK)
                        else:
                            return Response({'msg': "User Email Not Verified "}, status=HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'msg': 'User is Deactivated...!'}, status=HTTP_400_BAD_REQUEST)
                else:
                    if user.is_active:
                        if user.email_verified:
                            token = RefreshToken.for_user(user)
                            token = {
                                "access_token": str(token.access_token),
                                "refresh_token": str(token),
                                "is_active": user.is_active,
                                "message": "Login success",
                                "code": 200
                            }
                            return Response(token, status=HTTP_200_OK)
                        else:
                            return Response({'msg': 'Email Not Verified'}, status=HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'msg': 'User not activated'}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'User Not Found'}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            responce_data = {
                'msg': 'erorr',
                'error': e,
                'status': HTTP_400_BAD_REQUEST
            }
            return Response(responce_data, status=HTTP_400_BAD_REQUEST)


class LogoutView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def create(self,request,*args,**kwargs):
        data = request.data

        validate = validate_args(data, ['refresh_token'])
        if validate:
            return validate

        try:

            refresh_token = data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg':'LogedOut succsessfully'},status=HTTP_200_OK)


        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)

class ForgotPasswordView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            auth = RegisterAuthBackend()

            if not auth.email_verify(data['email']):
                return Response({'msg': 'Invalid Email'}, status=HTTP_400_BAD_REQUEST)

            user = Profile.objects.get(email__exact=data['email'])
            if user:
                if user.email_verified:
                    current_time = int(time.time())
                    user.email_otp = send_via_mail(data['email'])
                    user.email_otp_expired = current_time + 300
                    user.save()
                    return Response({'msg': 'Otp sent on email '}, status=HTTP_200_OK)

                else:
                    return Response({'msg': 'Email Not verified'})
            else:
                return Response({'msg': 'Invalid user'}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)



class EmailOtpVerifyView(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            validate = validate_args(data, ['email', 'otp'])
            if validate:
                return validate

            auth = RegisterAuthBackend()
            if not auth.email_verify(data['email']):
                return Response({'msg': 'Invalid Email'}, status=HTTP_400_BAD_REQUEST)

            user = Profile.objects.get(email__exact=data['email'])
            if user:
                current_time = int(time.time())

                if user.email_otp_expired >= current_time and user.email_otp == data['otp']:
                    return Response({'msg': 'Otp matched successfully...'}, status=HTTP_200_OK)
                else:
                    return Response({'msg': 'Invaild otp or Otp time expired...'}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'Invalid User'})

        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)





class ResendOtpView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            auth = RegisterAuthBackend()

            if not auth.email_verify(data['email']):
                return Response({'msg': 'Invalid Email'}, status=HTTP_400_BAD_REQUEST)

            user = Profile.objects.get(email__exact=data['email'])
            if user:
                if user.email_verified:
                    current_time = int(time.time())
                    user.email_otp = send_via_mail(data['email'])
                    user.email_otp_expired = current_time + 300
                    user.save()
                    return Response({'msg': 'Otp sent on email '}, status=HTTP_200_OK)

                else:
                    return Response({'msg': 'Email Not verified'})
            else:
                return Response({'msg': 'Invalid user'}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)




class NewPasswordView(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            validate = validate_args(data,['email','password','password2'])
            if validate:
                return validate
            auth = RegisterAuthBackend()

            if not auth.email_verify(data['email']):
                return Response({'msg':'Invalid Email','code':400},status=HTTP_400_BAD_REQUEST)

            if data['password'] and data['password'] != data['password2']:
                return Response({'msg':'Password and Confirmpassword are not matching ...','code':400},status=HTTP_400_BAD_REQUEST)


            try:
                user = Profile.objects.get(email__exact=data['email'], email_verified=True)

                if user:
                    user.set_password(data['password'])
                    user.save()
                    return Response({'msg': 'Password Reset Sucsessfully', 'Code': 201}, status=HTTP_201_CREATED)
                else:
                    return Response({'msg': 'User Not Found ', 'Code': 400}, status=HTTP_400_BAD_REQUEST)

            except Exception as e:
                response_data = {
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error': str(e),
                    'message': 'Something went wrong.'
                }
                return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(e)
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)




class DeleteProfile(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def create(self,request,*args,**kwargs):
        try:
            data = request.data
            validate = validate_args(data,['email','password'])
            if validate:
                return validate

            if not validate_email_address(data['email']):
                return Response({'msg':'Invalid format email id ','code':400},status=HTTP_400_BAD_REQUEST)

            obj = Profile.objects.get(email=data['email'],email_verified=True)
            if obj:
                obj.delete()
                return Response({'msg':'Profile deleted ....','code':200},status=HTTP_200_OK)
            else:
                return Response({'msg':'User not found','code':400},status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = {
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'error': str(e),
                'message': 'Something went wrong.'
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)

