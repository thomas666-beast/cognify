from django.contrib import admin
from .models import AntiSpyQuote


@admin.register(AntiSpyQuote)
class AntiSpyQuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_preview', 'author', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['quote', 'author']
    list_editable = ['is_active']

    def quote_preview(self, obj):
        return obj.quote[:50] + '...' if len(obj.quote) > 50 else obj.quote

    quote_preview.short_description = 'Quote'
