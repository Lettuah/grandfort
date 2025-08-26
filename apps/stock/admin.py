from django.contrib import admin
from .models import Stock
import logging
from ..daily_routine.models import DailyRoutine
from django.db import models

logger = logging.getLogger(__name__)

# Register your models here.
@admin.register(Stock)

class StockAdmin(admin.ModelAdmin):
    list_display = ['date_stocked', 'batch_id', 'category', 'breed' , 'stock_type', 'quantity_stocked', 'unit_price', 'total_cost_formated', 'total_mortality', 'total_sold', 'current_stock', 'supplier', 'facilitator', 'total_income', 'total_expenditure', 'gross_profit_loss', 'profit_loss_margin', 'reports']

    list_display_links = ['date_stocked','batch_id', 'total_cost_formated']
    
    
    
    def total_cost_formated(self, obj):
        """display total cost in human readable format"""
        if hasattr(obj, 'total_cost') and obj.total_cost is not None:
            return f"{obj.total_cost:,.2f}"
        return None

    total_cost_formated.short_description = 'Total Cost'

    # Get total_mortality from the daily routine for each batch stock
    # def get_total_mortality(self, obj):
    #     try:
    #         return DailyRoutine.objects.filter(stock=obj.id).aggregate(
    #             total_mortality=models.Sum('mortality')
    #         )['total_mortality'] or 0
           
    #     except Exception as e:
    #         logger.error(f"Error calculating total mortality for batch_id {obj.batch_id}: {str(e)}")
    #         return None
    # get_total_mortality.short_description = 'Total Mortality'

    # def get_current_stock(self, obj):
    #     if hasattr(obj, 'current_stock') and obj.current_stock is not None:
    #         return obj.current_stock
    # get_current_stock.short_description = "Current Stock"


