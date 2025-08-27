from django.db import models
from django.utils import timezone
from common.models import BaseModel
from django.core.validators import MinValueValidator
from django.db.models import Sum, F


# Create your models here.
class Income(BaseModel):
    PRODUCT_TYPES = [
        ("bird", "Bird"),
        ("fish", "Fish"),
    ]
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("ongooing", "Ongoing"),
    ]
    PAYMENT_MODE = [
        ("cash", "Cash"),
        ("transfer", "Transfer"),
        ("dual", "Cash & Transfer"),
    ]
    stock = models.ForeignKey(
        'stock.Stock',
        on_delete=models.CASCADE,
        related_name="stock_incomes",
    )
    product = models.CharField(
        choices=PRODUCT_TYPES,
        verbose_name="Product",
        help_text="What product type?",
        max_length=20,
    )
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1, "Cannot be zero or negative."),
        ],
        help_text="Total number of items",
    )
    weight = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        help_text="total weight in KG",
    )
    unit_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[
            MinValueValidator(1, "Cannot be zero or negative"),
        ],
        help_text="Per item price",
    )
    customer = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Who buys this product?'
    )
    payment_status = models.CharField(
        choices=PAYMENT_STATUS,
        default="pending",
        max_length=20,
    )
    payment_mode = models.CharField(
        choices=PAYMENT_MODE,
        blank=True,
        max_length=20,
        null=True,
        help_text='What is the payment method used?',
    )
    commenced_on = models.DateField(
        default=timezone.now,
    )
    completed_on = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.quantity} {self.product} - {self.stock}"

    def save(self, *args, **kwargs):
        #save to the db first
        super().save(*args, **kwargs)

    