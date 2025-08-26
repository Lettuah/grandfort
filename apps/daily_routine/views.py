from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib import messages

from apps.daily_routine.form import DailyRoutineForm
import logging


from apps.stock.models import Stock

logger = logging.getLogger(__name__)

# Create your views here.
def addRoutine(request):
    stocks = Stock.objects.all()
    if request.method == 'POST':
        form = DailyRoutineForm(request.POST)
        context = {
            'form': form, 'stocks': stocks
        }
        if not form.is_valid():
            messages.error(request, 'Invalid form submitted')
            return render(request, 'daily_routine/home.html', context)

        try:
            form.save()
            messages.success(request, "Record was successfully added")
            return redirect('daily-routine-home')
        except Exception as e:
            logger.error(form.errors)
            messages.error(request, f"Unable to process this form: {str(e)}")
            return render(request, 'daily_routine/home.html', context)

    else:
        form = DailyRoutineForm()
        context = {'form': form, 'stocks': stocks}
        return render(request, 'daily_routine/home.html', context)
