import sys

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from requests import Response
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

sys.path.append("D:\\python_pr\\sky_pro_f_pr\\todolist\\")

from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class VerificationView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def update(self, request, *args, **kwargs):
        serializer:  TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def perform_update(self, serializer):
        tg_user = serializer.save()
        TgClient(settings.BOT_TOKEN).send_message(
            chat_id=tg_user.chat_id,
            text='[verification has been complited]'
        )
