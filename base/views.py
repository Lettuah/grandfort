
from django.shortcuts import render
from  apps.daily_routine.models import DailyRoutine
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def home(request):

    
    return render(request, 'base/home.html')


def dashboard(request):
    routines = DailyRoutine.objects.all().order_by('-id')
    logger.info(f'ROUTINES : {routines}')
    
    context = {
        'routines': routines
    }
    return render(request, 'base/dashboard.html', context)