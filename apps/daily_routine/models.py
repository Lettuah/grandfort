
from django.db import models

from apps.stock.models import Stock
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging 

logger = logging.getLogger(__name__)

# Create your models here.
class DailyRoutine(models.Model):
    batch_id = models.ForeignKey(Stock, to_field='batch_id', on_delete=models.PROTECT, related_name='daily_routines')
    date = models.DateField(default=timezone.now, editable=False, help_text='Date of the routine entry')
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


    morning_water = models.PositiveBigIntegerField(help_text='Water given in liters (ltrs) in the morning')
    evening_water = models.PositiveBigIntegerField(help_text='Water given in liters (ltrs) in the evening')
    
    morning_medication = models.CharField(max_length=100, blank=True, help_text='Names of medication administered in the morning')
    evening_medication = models.CharField(max_length=100, blank=True, help_text='Names of medication administered in the evening')
    
    comment = models.TextField(blank=True, help_text='Additional notes or observations')


   

    def save(self, *args, **kwargs):
        """Calculate age before saving if not already set."""
        if not self.age:  # Only calculate if age is 0 (default)
            stock = self.batch_id
            date_stocked = stock.date_stocked
            date_now = timezone.now().date()
            self.age = (date_now - date_stocked).days
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def clean(self):
        """Validate the model data."""
        # Validate mortality against current_stock
        if hasattr(self, 'batch_id') and self.batch_id:
            try:
                # Assuming batch_id is a CharField, get the related Stock instance
                stock = Stock.objects.get(batch_id=self.batch_id.batch_id)
                current_stock = stock.current_stock  # Adjust if current_stock is a method
                logger.debug(f"Validating mortality: {self.mortality} vs current_stock: {current_stock}")
                if self.mortality > current_stock:
                    raise ValidationError("Mortality cannot exceed current stock.")
            except Stock.DoesNotExist as e:
                raise ValidationError(f"No Stock found for batch_id {self.batch_id}.") from e
            except AttributeError:
                raise ValidationError("Current stock not available for this batch.")

        # Validate unique batch_id and date combination
        if self.batch_id and self.date:
            existing_records = DailyRoutine.objects.filter(
                batch_id=self.batch_id,
                date=self.date
            ).exclude(pk=self.pk)  # Exclude current instance when editing
            if existing_records.exists():
                logger.warning(f"Duplicate batch_id {self.batch_id} and date {self.date} detected")
                raise ValidationError(
                    "A record for this batch ID and date already exists. Please edit the existing record."
                )
            logger.debug(f"No duplicate found for batch_id {self.batch_id} and date {self.date}")
       


    class Meta:
        verbose_name = "Daily Routine"
        verbose_name_plural = "Daily Routines"
        constraints = [
            models.UniqueConstraint(fields=['batch_id', 'date',], name='unique_batch_id_date')
        ]

    def __str__(self):
        return f"{self.batch_id} - {self.date}"