from django.contrib import admin
from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'get_full_name', 'position', 'email', 'is_active', 'date_joined']
    list_filter = ['position', 'is_active', 'date_joined']
    search_fields = ['nickname', 'firstname', 'lastname', 'email']
    list_editable = ['is_active']
    readonly_fields = ['date_joined', 'last_updated']

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = 'Full Name'
