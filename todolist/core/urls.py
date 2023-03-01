from django.contrib import admin
from django.urls import path

from core import views

# from django.contrib.auth import views



urlpatterns = [
    path('login', views.UserLogonView.as_view()),
    path('profile',views.UserRetrieveUpdateDestroyView.as_view() ),
    path('signup', views.UserCreateView.as_view()),
    path('update_password', views.PasswordUpdateAPIView.as_view(),)
]
