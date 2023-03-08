import sys

from django.urls import path

sys.path.append("D:\\python_pr\\sky_pro_f_pr\\todolist\\")
from bot import views


urlpatterns = [
    path("verify", views.VerificationView.as_view()),
]