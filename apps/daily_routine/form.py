
from django import forms

from apps.daily_routine.models import DailyRoutine
from apps.stock.models import Stock


class DailyRoutineForm(forms.ModelForm):
    mortality = forms.IntegerField(help_text="Number of bird found dead today", required=False)
    morning_feed = forms.IntegerField(help_text="Number of rubber of feed", required=False)
    morning_water = forms.IntegerField(help_text="Litres of water", required=False)
    morning_medication = forms.CharField(max_length=50, help_text="Names of drug mixed with water", required=False)

    evening_feed = forms.IntegerField(help_text="Number of rubber of feed", required=False)
    evening_water = forms.IntegerField(help_text="Litres of water", required=False)
    evening_medication = forms.CharField(max_length=50, help_text="Names of drug mixed with water", required=False)


    class Meta:
        model = DailyRoutine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.all()
        self.fields['stock'].widget.attrs.update({
            'class': 'form-select',
            'required': 'required'
        })