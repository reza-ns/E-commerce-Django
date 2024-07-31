from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'date_joined', 'is_active', 'is_staff', 'is_superuser']


admin.site.register(User, UserAdmin)

