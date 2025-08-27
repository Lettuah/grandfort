from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Sum, F
from django.apps import apps
Income = apps.get_model('income', 'Income')

@receiver([post_save, post_delete], sender=Income)
def update_stock_total_income_signal(sender, instance, **kwargs):
    stock = instance.stock
    total_income = get_stock_total_income_from_db(stock)
    total_sold = get_stock_total_sold_from_db(stock)

    stock.total_income      = total_income
    stock.total_sold        = total_sold
    stock.current_stock     = stock.quantity_stocked - stock.total_mortality - stock.total_sold
    stock.save(update_fields=["total_income", "total_sold", "current_stock"])


def get_stock_total_income_from_db(stock):
    return Income.objects.filter(stock=stock).aggregate(
        total_income=Sum(F("unit_price") * F("weight"))
    )["total_income"] or 0

def get_stock_total_sold_from_db(stock):
    return Income.objects.filter(stock=stock).aggregate(
        total_sold=Sum('quantity')
    )["total_sold"] or 0

