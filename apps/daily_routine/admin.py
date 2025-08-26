from django.contrib import admin
from .models import DailyRoutine

# Register your models here.


@admin.register(DailyRoutine)
class DailyRoutineAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "stock_batch_id_value",
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

    list_display_links = [
        "date",
        "stock_batch_id_value",
    ]

    fieldsets = (
        ("General", {"fields": ("date", "stock", "feed_type", "mortality"),}),
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
        ("Optional", {"fields": ("comment",)}),
    )

    def stock_batch_id_value(self, obj):
        """Return only the stock batch_id value."""
        return obj.stock.batch_id if obj.stock else None

    stock_batch_id_value.short_description = "Batch ID"
