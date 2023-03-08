from django.contrib import admin
from bot.models import TgUser

admin.register(TgUser)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user')
    search_fields = ['username', 'user']
    readonly_fields = ('chat_id', 'verification_code')