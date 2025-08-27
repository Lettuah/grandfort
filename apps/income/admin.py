from django.contrib import admin
from . models import Income
from common.utils import format_price

# Register your models here.
@admin.register(Income)


class IconAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'quantity',
        'weight',
        'formatted_unit_price',
        'formatted_total_revenue',
        'customer',
        'payment_status',
        'payment_mode',
        'commenced_on',
        'completed_on',
        'stock',
    ]

    list_display_links = [
        'product',
        'formatted_total_revenue',
        'stock',
    ]


    def formatted_unit_price(self, obj):
        if hasattr(obj, 'unit_price'):
            return format_price(obj.unit_price) or 0
        return None
    formatted_unit_price.short_description = 'Unit Price'
    
    
    def formatted_total_revenue(self, obj):
        if hasattr(obj, 'unit_price') and hasattr(obj, 'weight'):
            total = obj.unit_price * obj.weight
            return format_price(total) or 0
        return None
    formatted_total_revenue.short_description = 'Total Revenue'