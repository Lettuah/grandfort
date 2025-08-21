from django.db import models
from django.core.exceptions import ValidationError

class Stock(models.Model):
    date_stocked = models.DateField(auto_now_add=True, help_text='Date the stock was added')
    batch_id = models.CharField(max_length=50, unique=True, help_text='Unique identifier for the batch')
    
    STOCK_CATEGORIES = [
        ('poultry', 'Poultry'),
        ('fish', 'Fish'),
        ('goat', 'Goat'),
    ]
    category = models.CharField(choices=STOCK_CATEGORIES, max_length=50, default='poultry', help_text='Category of livestock')

    BREEDS = [
        ('broiler', 'Broiler'),
        ('noiler', 'Noiler'),
        ('clarias', 'Clarias'),
        ('hybrid', 'Hybrid'),
    ]
    breed = models.CharField(max_length=20, choices=BREEDS, default='broiler', help_text='Breed of the stock')

    STOCK_TYPES = [
        ('day_old_chick', 'Day-Old Chick'),
        ('fingerling', 'Fingerling'),
        ('juvenile', 'Juvenile'),
        ('grower', 'Grower'),
        ('adult_broiler', 'Adult Broiler'),
        ('point_of_lay', 'Point of Lay'),
    ]
    stock_type = models.CharField(max_length=20, choices=STOCK_TYPES, default='day_old_chick', help_text='Life stage of the stock')

    quantity_stocked = models.PositiveIntegerField(verbose_name='Quantity', help_text='Initial quantity stocked')
    total_mortality = models.PositiveIntegerField(default=0, verbose_name='Mortality', help_text='Total deaths recorded', blank=True)
    total_sold = models.PositiveIntegerField(default=0, verbose_name='Sold', help_text='Total quantity sold')
    supplier = models.CharField(max_length=50, blank=True, help_text='Name of the supplier')
    facilitator = models.CharField(max_length=50, blank=True, help_text='Name of the facilitator')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per unit in currency')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)


    @property
    def current_stock(self):
        return self.quantity_stocked - self.total_mortality - self.total_sold

    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Total income from sales')
    total_expenditure = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Total expenditure')

    @property
    def gross_profit_loss(self):
        return self.total_income - self.total_cost - self.total_expenditure

    @property
    def profit_loss_margin(self):
        if self.total_cost != 0:
            return (self.gross_profit_loss / self.total_cost) * 100
        return 0

    # Weekly reports as a single model or JSON field for flexibility
    reports = models.JSONField(default=dict, blank=True, help_text='Weekly reports in JSON format')

    def clean(self):
        """Validate fields before saving."""
        if self.unit_price is None or self.quantity_stocked is None:
            raise ValidationError("Unit price and quantity stocked must not be None.")
        if self.unit_price < 0 or self.quantity_stocked < 0:
            raise ValidationError("Unit price and quantity stocked must not be negative.")

    def calculate_total_cost(self):
        """Calculate the total cost based on unit price and quantity stocked."""
        self.total_cost = self.unit_price * self.quantity_stocked

    def form_batch_id(self):
        ...

    def save(self, *args, **kwargs):
        """Override save to enforce validation."""
        self.clean()
        self.calculate_total_cost() # get totoal const
        super().save(*args, **kwargs)

   

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.batch_id} - {self.category} ({self.current_stock} remaining)"