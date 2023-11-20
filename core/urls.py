from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

core = DefaultRouter()

core.register('PostView',PostView,basename='PostView')
core.register('VideoPostView',VideoPostView,basename='VideoPostView')
core.register('HighlightsView',HighlightsView,basename='HighlightsView')
core.register('LikeView',LikeView,basename='LikeView')
core.register('StoriesView',StoriesView,basename='StoriesView')
core.register('CommentsViewset',CommentsViewset,basename='CommentsViewset')
core.register('FollowingViewSet',FollowingViewSet,basename='FollowingViewSet')
# core.register('CommentsCountView',CommentsCountView,basename='CommentsCountView')

urlpatterns = [
    path('',include(core.urls)),
]