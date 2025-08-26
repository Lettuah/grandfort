
from django.db import models

from apps.stock.models import Stock
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging 
from django.db.models import Sum 
logger = logging.getLogger(__name__)

# Create your models here.
class DailyRoutine(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_daily_routine')
    date = models.DateField(default=timezone.now, editable=True, help_text='Date of the routine entry')
    mortality = models.PositiveIntegerField(default=0, help_text='Number of deaths recorded (default: 0)')
    age = models.PositiveIntegerField(default=0, editable=False)

    FEED_TYPES = [
        ('pellet', 'Pellet'),
        ('mash', 'Mash'),
        ('crumble', 'Crumble'),
    ]

    feed_type = models.CharField(choices=FEED_TYPES, max_length=50, blank=True, help_text='The type of feed given')
    morning_feed = models.PositiveIntegerField(default=0, help_text='Number of 20-liter containers of feed in the morning')
    evening_feed = models.PositiveIntegerField(default=0, help_text='Number of 20-liter containers of feed in the evening')


    morning_water = models.PositiveBigIntegerField(default=0, help_text='Water given in liters (ltrs) in the morning')
    evening_water = models.PositiveBigIntegerField(default=0, help_text='Water given in liters (ltrs) in the evening')
    
    morning_medication = models.CharField(max_length=100, blank=True, help_text='Names of medication administered in the morning')
    evening_medication = models.CharField(max_length=100, blank=True, help_text='Names of medication administered in the evening')
    
    comment = models.TextField(blank=True, help_text='Additional notes or observations')


    def save(self, *args, **kwargs):
        """Calculate age before saving if not already set."""
        if not self.age:
            stock = self.stock
            date_stocked = stock.date_stocked
            date_now = timezone.now().date()
            self.age = (date_now - date_stocked).days
        """Update the current stock"""
        stock = self.stock #instance of this stock
        stock.current_stock = stock.quantity_stocked - stock.total_sold - self.get_total_mortality()
        stock.save()
       
        
        """Run the clean method for validation"""
        self.clean()  # Validate before saving
        
        super().save(*args, **kwargs)

    def clean(self):
        """Validate the model data."""
        if not hasattr(self, 'stock') or not self.stock:
            raise ValidationError('Record could not be completed. Batch ID is missing')

        try:
            # Assuming batch_id is a CharField, get the related Stock instance
            stock = self.stock # this stock instance
            current_stock = stock.current_stock
            logger.debug(f"Validating mortality: {self.mortality} vs current_stock: {current_stock}")
            if self.mortality > current_stock:
                raise ValidationError("Mortality cannot exceed current stock.")
        except Stock.DoesNotExist as e:
            raise ValidationError(f"No Stock found for batch_id {self.stock}.") from e
        except AttributeError as e:
            raise ValidationError("Current stock not available for this batch.") from e
        # Validate unique batch_id and date combination
        if self.stock and self.date:
            existing_records = DailyRoutine.objects.filter(
                stock=self.stock,
                date=self.date
            ).exclude(pk=self.pk)  # Exclude current instance when editing
            if existing_records.exists():
                logger.warning(f"Duplicate batch_id {self.stock} and date {self.date} detected")
                raise ValidationError(
                    "A record for this batch ID and date already exists. Please edit the existing record for update."
                )
        else: 
            logger.error(f'STOCK: {self.stock} and DATE: {self.date}')
            raise ValidationError('Something is wrong with batch id and date.')
        
    
    def get_total_mortality(self):
        """
        Returns the total mortality recorded for this stock across all DailyRoutine entries.
        Always returns an integer (0 if no mortality recorded).
        """
        try:
            total = self._get_total_mortality_from_db()
            _total_mortality = total + self.mortality if total is not None else self.mortality
    
            # Update the stock model
            stock = self.stock
            stock.total_mortality = _total_mortality
            stock.save()
    
            return _total_mortality  # Ensure we always return an integer
        except Exception as e:
            # Better to log than print in production
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Could not calculate total mortality for stock {self.stock}: {str(e)}")
            return 0
    
    def _get_total_mortality_from_db(self):
        """
        Sum mortality for all DailyRoutine entries of this stock.
        """
        return DailyRoutine.objects.filter(stock=self.stock).aggregate(
            total_mortality=Sum('mortality')
        )['total_mortality']


    class Meta:
        verbose_name = "Daily Routine"
        verbose_name_plural = "Daily Routines"
        constraints = [
            models.UniqueConstraint(fields=['stock', 'date',], name='unique_stock_date')
        ]

    def __str__(self):
        return f"{self.stock} - {self.date}"