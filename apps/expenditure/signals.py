from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Sum, F
from django.apps import apps
Expenditure = apps.get_model('expenditure', 'Expenditure')

@receiver([post_save, post_delete], sender=Expenditure)
def update_stock_total_expenditure_signal(sender, instance, **kwargs):
    stock = instance.stock
    total = get_stock_total_expenditure_from_db(stock)

    stock.total_expenditure = total
    stock.save(update_fields=["total_expenditure"])


def get_stock_total_expenditure_from_db(stock):
    return Expenditure.objects.filter(stock=stock).aggregate(
        total_expenditure=Sum(F("unit_cost") * F("quantity"))
    )["total_expenditure"] or 0