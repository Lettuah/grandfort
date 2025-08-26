from . import views

from django.urls import include, path

urlpatterns = [
     path('', views.home, name='home'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('account/', include('apps.accounts.urls'), name='account_app'),
     path('daily-routine/', include('apps.daily_routine.urls'), name='daily_routine_app'),
]