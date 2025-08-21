from django.contrib import admin
from .models import DailyRoutine

# Register your models here.


@admin.register(DailyRoutine)
class DailyRoutineAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "batch_id_value",
        "mortality",
        "age",
        "feed_type",
        "morning_feed",
        "evening_feed",
        "morning_water",
        "morning_water",
        "morning_medication",
        "evening_medication",
    ]
    exclude = []

    fieldsets = (
        ("General", 
         {
            "fields": ("batch_id","feed_type", "mortality")
        }
        ),
        (
            "Morning Phase",
            {
                "fields": ("morning_feed", "morning_water", "morning_medication"),
            },
        ),
        (
            "Evening Phase",
            {
                "fields": ("evening_feed", "evening_water", "evening_medication"),
            },
        ),
        ('Optional', {
            'fields': ('comment',)
        }),
    )

    def batch_id_value(self, obj):
        """Return only the batch_id value."""
        return obj.batch_id.batch_id if obj.batch_id else None

    batch_id_value.short_description = "Batch ID"  # Custom column header
