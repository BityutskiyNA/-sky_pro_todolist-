import sys

from django.contrib import admin

# from todolist.bot.models import TgUser
sys.path.append("D:\\python_pr\\sky_pro_f_pr\\todolist\\")
from bot.models import TgUser

admin.register(TgUser)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    ...