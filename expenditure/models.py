from django.db import models
from django.utils import timezone
from django.contrib import admin

class ExpenseType(models.Model):
    expense_title = models.CharField(
        max_length=250,
        help_text="Name of the expense category (e.g., Office Supplies, Transport, Rent)."
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['expense_title']

    def save(self, *args, **kwargs):
        if not self.pk:  # Only run for new records
            base_title = self.expense_title.strip()

            # Find how many entries start with the same title
            existing_count = ExpenseType.objects.filter(
                expense_title__startswith=base_title
            ).count()

            # If it's not the first one, append number
            if existing_count > 0:
                self.expense_title = f"{base_title} #{existing_count + 1}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.expense_title


class ExpenditureAdmin(admin.ModelAdmin):
    fieldform = [
        {"fields" : { "item_name", "supplier",}}
    ]

class Expenditure(models.Model):
    expense_type = models.ForeignKey(
        ExpenseType,
        on_delete=models.PROTECT,
        related_name="expenditures",
        help_text="Select the category for this expense."
    )
    item_name = models.CharField(max_length=250)
    supplier = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2,editable=False)
    note = models.TextField(blank=True)
    date_recorded = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Auto-calculate total cost if not provided
        
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} ({self.expense_type})"
