from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate



# Create your views here.
def login(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request)
        if form.is_valid:
            if auth := authenticate(form):
                return redirect('home')
        
        messages.error(request, 'Invalid credentials')

    return render(request, 'login.html', {'form': form})

def register(request):
    form = UserCreationForm()
    if request.method == 'post':
        form = UserCreationForm(request.post)
        if form.is_valid:
            form.save
            messages.success(request, 'Registraion was successful')
            return redirect('home')
        messages.error(request, 'error occurs')
    return render(request, 'register.html', {'form': form})
