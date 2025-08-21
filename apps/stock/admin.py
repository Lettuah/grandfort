from django.contrib import admin
from .models import Stock
import logging
from ..daily_routine.models import DailyRoutine
from django.db import models

logger = logging.getLogger(__name__)

# Register your models here.
@admin.register(Stock)

class StockAdmin(admin.ModelAdmin):
    list_display = ['date_stocked', 'batch_id', 'category', 'breed' , 'stock_type', 'quantity_stocked', 'unit_price', 'total_cost_formated', 'get_total_mortality', 'total_sold', 'get_current_stock', 'supplier', 'facilitator', 'total_income', 'total_expenditure', 'gross_profit_loss', 'profit_loss_margin', 'reports']

    list_display_links = ['date_stocked','batch_id', 'total_cost_formated']
    
    
    
    def total_cost_formated(self, obj):
        """display total cost in human readable format"""
        if hasattr(obj, 'total_cost') and obj.total_cost is not None:
            return f"{obj.total_cost:,.2f}"
        return None

    total_cost_formated.short_description = 'Total Cost'

    # Get total_mortality from the daily routine for each batch stock
    def get_total_mortality(self, obj):
        try:
            mortality = DailyRoutine.objects.filter(batch_id=obj.batch_id).aggregate(
                total_mortality=models.Sum('mortality')
            )['total_mortality'] or 0
            logger.debug(f"Total mortality for batch_id {obj.batch_id}: {mortality}")
            return mortality
        except Exception as e:
            logger.error(f"Error calculating total mortality for batch_id {obj.batch_id}: {str(e)}")
            return None
    get_total_mortality.short_description = 'Total Mortality'

    def get_current_stock(self, obj):
        try:
            return obj.quantity_stocked -  self.get_total_mortality(obj) - obj.total_sold
        except Exception as e:
            logger.error(f'COULD NOT GET THE CURRENT STOCK: {str(e)}')
            return None
    get_current_stock.short_description = "Current Stock"


