
from django.utils import timezone
import random, string, logging
from django.db import models
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)
class Stock(models.Model):
    date_stocked = models.DateField(auto_now_add=True, help_text='Date the stock was added')
    batch_id = models.CharField(max_length=50, unique=True, editable=False, help_text='Unique identifier for the batch')
    
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
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per unit in currency')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    total_mortality = models.PositiveIntegerField(default=0, verbose_name='Mortality', help_text='Total deaths recorded',editable=False, blank=True)
    total_sold = models.PositiveIntegerField(default=0, verbose_name='Sold', editable=False, help_text='Total quantity sold')
    current_stock = models.PositiveIntegerField(default=0, verbose_name='Current Stock', editable=False, help_text='Total available stock')

    supplier = models.CharField(max_length=50, blank=True, help_text='Name of the supplier')
    facilitator = models.CharField(max_length=50, blank=True, help_text='Name of the facilitator')
   
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False, help_text='Total income from sales')
    total_expenditure = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False, help_text='Total expenditure')

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

   
    def form_batch_id(self):
        """Generate a unique batch ID based on category, breed, random code, month, and year."""
        if not self.category or not self.breed:
            raise ValidationError("Category and breed must be set before generating batch_id.")

        # Get initials: first letter of category, first three letters of breed
        category_initial = self.category[:1].upper() if self.category else 'X'
        breed_initial = (self.breed[:3].upper() if len(self.breed) >= 3 else self.breed.upper().ljust(3, 'X'))

        # Get month and year from date_stocked or current time
        date = self.date_stocked or timezone.now().date()
        month = date.strftime("%b").upper()  # e.g., JUL
        year = date.year  # e.g., 2025

        # Generate random 6-character code (uppercase letters and digits)
        characters = string.ascii_uppercase + string.digits
        max_attempts = 10
        for _ in range(max_attempts):
            random_code = ''.join(random.choices(characters, k=6))
            batch_id = f"{category_initial}-{breed_initial}-{random_code}-{month}-{year}"
            # Check for uniqueness
            if not Stock.objects.filter(batch_id=batch_id).exists():
                return batch_id
        raise ValidationError("Could not generate a unique batch_id after multiple attempts.")

    def save(self, *args, **kwargs):
        """Override save to enforce validation."""
        self.clean()
        self.total_cost =  self.unit_price * self.quantity_stocked
        if not self.batch_id:
            self.batch_id = self.form_batch_id()
        # set current stock to quality_stocked @ initial
        if not self.pk:
            self.current_stock = self.quantity_stocked
        
    
        super().save(*args, **kwargs)

       

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.batch_id} - {self.category}"
    