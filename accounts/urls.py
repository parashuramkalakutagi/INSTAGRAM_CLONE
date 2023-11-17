
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

account = DefaultRouter()

account.register('singup',SingUpViewset,basename='singup')
account.register('Verify_Email',Verify_Email,basename='Verify_Email')
account.register('Delete_EmailUser',Delete_EmailUser,basename='Delete_EmailUser')
account.register('LoginView',LoginView,basename='LoginView')
account.register('LogoutView',LogoutView,basename='LogoutView')
account.register('ForgotPasswordView',ForgotPasswordView,basename='ForgotPasswordView')
account.register('EmailOtpVerifyView',EmailOtpVerifyView,basename='EmailOtpVerifyView')
account.register('ResendOtpView',ResendOtpView,basename='ResendOtpView')
account.register('NewPasswordView',NewPasswordView,basename='NewPasswordView')


urlpatterns = [
    path('',include(account.urls)),
]