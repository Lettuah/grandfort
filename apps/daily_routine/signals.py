from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Sum, F
from django.apps import apps
DailyRoutine = apps.get_model('daily_routine', 'DailyRoutine')

@receiver([post_save, post_delete], sender=DailyRoutine)
def update_stock_total_income_signal(sender, instance, **kwargs):
    stock = instance.stock
    total_mortality = get_stock_total_mortality_from_db(stock)
    stock.total_mortality      = total_mortality
    stock.current_stock = stock.quantity_stocked - stock.total_sold -stock.total_mortality
    stock.save(update_fields=["total_mortality", "current_stock"])


def get_stock_total_mortality_from_db(stock):
    return DailyRoutine.objects.filter(stock=stock).aggregate(
        total_mortality=Sum("mortality")
    )["total_mortality"] or 0

