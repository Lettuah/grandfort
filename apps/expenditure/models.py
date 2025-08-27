from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum , F
import uuid

class Expenditure(models.Model):

    stock = models.ForeignKey(
        'stock.Stock',
        on_delete=models.CASCADE,
        related_name='expenditures', 
        verbose_name='Stock'
    )
    item = models.CharField(
        max_length=50,
        verbose_name='Item Name/Title',
    )
    reference = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Ref Code", unique=True)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1, message='Quantity must be at least 1.')],
        verbose_name='Quantity'
    )
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1, message='Unit cost cannot be zero or negative.')],
        verbose_name='Unit Cost'
    )
    seller = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Seller/Store',
        help_text='Name of the seller, store, or person paid for this expenditure.'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Any information regarding this item?'
    )
    date_purchased = models.DateField(
        default=timezone.now,  # Simplified default
        verbose_name='Date Purchased'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date Created'
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Date Updated'
    )

    def __str__(self):
        return f"{self.item} ({self.quantity}) - {self.stock} on {self.date_purchased}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the total expenditure
        # self.update_stock_total_expenditure()

    class Meta:
        verbose_name = 'Expenditure'
        verbose_name_plural = 'Expenditures'
        ordering = ['-date_purchased', 'item']
    
    # def get_total_expenditure_from_db(self):
    #     """
    #     Returns the total expenditure for this stock from the DB.
    #     """
    #     result = Expenditure.objects.filter(stock=self.stock).aggregate(
    #         total_expenditure=Sum(F("unit_cost") * F("quantity"))
    #     )
    #     return result["total_expenditure"] or 0

    # def update_stock_total_expenditure(self):
    #     """
    #     Updates the stock's total_expenditure field by recalculating from DB.
    #     """
        
    #     old_total = self.get_total_expenditure_from_db()
    #     # New record
    #     if not self.pk:
    #         new_total = old_total +  (self.unit_cost * self.quantity)

    #     else:
    #         # Update existing reocr
    #         this_record = Expenditure.objects.get(pk=self.pk)
    #         old_value = this_record.unit_cost * this_record.quantity
    #         new_total = (old_total - old_value) + (self.unit_cost * self.quantity)

    #     stock = self.stock
    #     stock.total_expenditure = new_total
    #     stock.save(update_fields=["total_expenditure"])
        