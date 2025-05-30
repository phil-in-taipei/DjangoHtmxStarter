from django.contrib import admin
from .models import Thing


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_profile', 'created_at', 'updated_at']
    list_filter = ['created_at', 'user_profile']
    search_fields = ['name', 'description', 'user_profile__user__username']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'user_profile')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
