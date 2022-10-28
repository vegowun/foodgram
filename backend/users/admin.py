from django.contrib import admin

from users.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'
