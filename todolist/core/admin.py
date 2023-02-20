from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User

# Register your models here.
# admin.site.register(User)
@admin.register(User)
class UserAdmin(UserAdmin):
    # inlines = (GenreFilmworkInline, PersonFilmworkInline,)
    # # Отображение полей в списке
    list_display = ('username', 'email', 'first_name','last_name')

    # Фильтрация в списке
    list_filter = ('is_staff','is_active', 'is_superuser',)

    search_fields = ('emailfirst_name', 'last_name', 'username')

    exclude = ['password']
    readonly_fields = ['last_login', 'date_joined',]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Особые даты', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.unregister(Group)