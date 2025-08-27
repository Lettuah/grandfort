from django.contrib import admin
from . models import Expenditure
from common.utils import format_price

# Register your models here.
@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = [
        "item",
        "quantity",
        "formatted_unit_cost",
        "total_cost",
        "date_purchased",
        "date_created",
        "date_updated",
        "stock"
    ]


    def formatted_unit_cost(self, obj):
        return format_price(getattr(obj, 'unit_cost', None))
    formatted_unit_cost.short_description = 'Unit Cost'

    def total_cost(self, obj):
        if hasattr(obj, 'unit_cost') and hasattr(obj, 'quantity'):
            total = obj.unit_cost * obj.quantity
            return format_price(total)
        return None

    total_cost.short_description = "Total Cost"

    