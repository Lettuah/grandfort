
from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True, label='Password', )
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='Password confirmation')


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True, label='Password', )