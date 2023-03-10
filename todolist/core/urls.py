from django.urls import path

from core import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login', csrf_exempt(views.UserLogonView.as_view()), name='login'),
    path('profile', views.UserRetrieveUpdateDestroyView.as_view()),
    path('signup', csrf_exempt(views.UserCreateView.as_view())),
    path('update_password', csrf_exempt(views.PasswordUpdateAPIView.as_view())),
]
