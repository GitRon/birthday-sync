from django.contrib import admin

from birthday_sync.models import GoogleContact


@admin.register(GoogleContact)
class GoogleContactAdmin(admin.ModelAdmin):
    list_display = ("google_id", "name")
    search_fields = ("google_id", "name")
