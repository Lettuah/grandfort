from django.urls import path

from apps.daily_routine import views


urlpatterns = [
    path('', views.addRoutine, name='daily-routine-home'),
    # path('add/', views.addRoutine, name='add-routine')
]