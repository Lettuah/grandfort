
from django.http import HttpRequest
from django.shortcuts import redirect, render

from base.views import home
from .models import PendingUser, CustomUser
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from common.tasks import send_email
from django.contrib import messages, auth
from . forms import RegistrationForm, LoginForm

import logging

logger = logging.getLogger(__name__)

# Ensure logger outputs to the console for debugging
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# Create your views here.

def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('home')

def login(request: HttpRequest):
    if request.method != 'POST':
        return render(request, 'login.html')

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {'form': form})

    email = form.cleaned_data['email'].lower()
    password = form.cleaned_data['password']

    logger.info(f'YOUR EMAIL IS: {email}')

    user = auth.authenticate(request.POST, email=email, password=password)
    if user is not None:
        # if record is confirmed matched the database
        # login the user
        auth.login(request, user)
        messages.success(request, 'You are signed in.')
        return redirect('home')

    messages.error(request, 'Invalid credentials')
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        # if method is post, collect form data
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            logger.info('THE FORM IS VALID')
            email : str = request.POST['email'].lower()
            password: str = request.POST['password1']
            password_confirmation: str = request.POST['password2']
            cleaned_email = email.lower()
            
            if password != password_confirmation:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'register.html', {'form': form})

            # validate input

            # Check if email already exist
            if CustomUser.objects.filter(email = cleaned_email).exists():
                # session message
                messages.error(request, 'Email address already used')
                return redirect('register')
            else:
                # email is not used before
                verification_code = get_random_string(10)
                # Use update_or_create to ensure a PendingUser entry is created or updated for this email,
                # preventing duplicate pending users and handling repeated registration attempts gracefully.
                PendingUser.objects.update_or_create(
                    email = cleaned_email,
                    defaults={
                        "verification_code": verification_code,
                        "password": make_password(password)
                    }
                )
                logger.info(f'VERIFICATION CODE SENT: {verification_code}')
                # send verification code to email
                # send_email(
                #     'Email Verification',
                #     f'Your verification code is: {verification_code}',
                #     [cleaned_email],
                #     "info@alayopay.ng",
                # )

                # session message
                messages.success(request, f'Verification code sent to your email: {cleaned_email}')

                # redirect to email verification page
                return render(request, 'email_verification.html', {'email': cleaned_email})
        else:
            logger.info('INVALID FORM')
            logger.error(form.errors)
            return render (request, 'register.html', {'form': form})
            
        ...
    # If not post method
    return render (request, 'register.html')


# Email verification
def create_user_from_pending(pending_user):
    user = CustomUser.objects.create(
        email=pending_user.email,
        password=pending_user.password
    )
    user.save()
    pending_user.delete()
    return user

def email_verification(request):
    if request.method != "POST":
        return render(request, 'email_verification.html', status=501)

    code = request.POST['code']
    email = request.POST['email']
    pending_user = PendingUser.objects.filter(verification_code=code, email=email).first()
    if pending_user and pending_user.is_valid:
        user = create_user_from_pending(pending_user)
        auth.login(request, user)
        messages.success(request, 'Your account was verified successfully')
        return redirect(home)

    messages.error(request, 'Invalid or expired verification code entered')
    return render(request, 'email_verification.html', {'email': email})