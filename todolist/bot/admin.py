import sys

from django.contrib import admin

sys.path.append("D:\\python_pr\\sky_pro_f_pr\\todolist\\")
from bot.models import TgUser

admin.register(TgUser)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user')
    search_fields = ['username', 'user']
    readonly_fields = ('chat_id', 'verification_code')