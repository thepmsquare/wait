from django.contrib import admin

from .models import UserSettings, WeightEntry


@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "weight", "unit", "timestamp")
    list_filter = ("unit", "timestamp")
    search_fields = ("user__username", "user__email")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "target_weight", "preferred_unit")
    search_fields = ("user__username", "user__email")
