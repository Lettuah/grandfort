from django.contrib import admin
from .models import Stock
import logging
from common.utils import format_price

logger = logging.getLogger(__name__)


# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [
        "date_stocked",
        "batch_id",
        "category",
        "breed",
        "stock_type",
        "quantity_stocked",
        "unit_price",
        "total_cost_formated",
        "total_mortality",
        "total_sold",
        "current_stock",
        "supplier",
        "facilitator",
        "formatted_total_income",
        "formatted_total_expenditure",
        "gross_profit_loss",
        "profit_loss_margin",
        "reports",
    ]

    list_display_links = [
        "date_stocked",
        "batch_id",
        "total_cost_formated",
    ]

    def total_cost_formated(self, obj):
        """display total cost in human readable format"""
        if hasattr(obj, "total_cost") and obj.total_cost is not None:
            return format_price(obj.total_cost)
        return None

    total_cost_formated.short_description = "Total Cost"

    def formatted_total_expenditure(self,obj):
        if hasattr(obj, 'total_expenditure'):
            return format_price(obj.total_expenditure)
        return None
    formatted_total_expenditure.short_description = 'Total Expenditure'

    def formatted_total_income(self, obj):
        if hasattr(obj, 'total_income'):
            return format_price(obj.total_income) or 0
        return None
    formatted_total_income.short_description = 'Total Income'
