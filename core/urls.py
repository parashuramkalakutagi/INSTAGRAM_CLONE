from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

core = DefaultRouter()

core.register('PostView',PostView,basename='PostView')

urlpatterns = [
    path('',include(core.urls)),
]