from django.contrib import admin
from .models import Master

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active', 'date_joined', 'last_login']
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username']
    readonly_fields = ['date_joined', 'last_login']
