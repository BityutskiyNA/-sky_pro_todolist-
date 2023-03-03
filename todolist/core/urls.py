from django.contrib import admin
from django.urls import path

from core import views
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# from django.contrib.auth import views
# path('profile', csrf_exempt(views.UserRetrieveUpdateDestroyView.as_view())),


urlpatterns = [
    path('login', csrf_exempt(views.UserLogonView.as_view())),
    path('profile',csrf_exempt(views.UserRetrieveUpdateDestroyView.as_view() )),
    path('signup', csrf_exempt(views.UserCreateView.as_view()) ),
    path('update_password', csrf_exempt(views.PasswordUpdateAPIView.as_view())),
]
