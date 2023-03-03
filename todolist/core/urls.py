from django.contrib import admin
from django.urls import path

from core import views
from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth import views



urlpatterns = [
    path('login', csrf_exempt(views.UserLogonView.as_view())),
    path('profile',csrf_exempt(views.UserRetrieveUpdateDestroyView.as_view() )),
    path('signup', views.UserCreateView.as_view()),
    path('update_password', csrf_exempt(views.PasswordUpdateAPIView.as_view())),
]
