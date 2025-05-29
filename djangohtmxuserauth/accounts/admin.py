from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'given_name', 'surname', 'serial_number']
    readonly_fields = ['serial_number']

