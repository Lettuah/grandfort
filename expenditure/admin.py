from django.contrib import admin

from expenditure.models import Expenditure, ExpenseType

# Register your models here.
admin.site.register([Expenditure, ExpenseType])
