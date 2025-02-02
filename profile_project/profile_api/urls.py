"""
Include the URL configuration for Profile APIs
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('hello-vs', views.HelloViewSet, basename='hello-vs')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.ProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloAPIView.as_view()),
    path('login/', views.UserLoginAPIView.as_view()),
    path('', include(router.urls))
]
