from django.contrib import admin
from .models import Orbit

@admin.register(Orbit)
class OrbitAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status', 'order', 'color', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['status', 'order']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Configuration', {
            'fields': ('status', 'order', 'color', 'icon')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
