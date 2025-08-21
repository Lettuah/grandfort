from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from common.models import BaseModel
from .manager import CustomUserManager




class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
   
        

class PendingUser(BaseModel):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self) -> bool:
        """Checks if the PendingUser is still valid based on its creation time.

        Returns True if the user was created within the last 30 minutes, otherwise False.

        Returns:
            bool: True if valid, False otherwise.
        """
        lifespan_in_seconds = 30 * 60

        # Use Django's timezone-aware datetime for consistency
        now = timezone.now()

        time_diff = (now - self.created_at).total_seconds()

        return time_diff <= lifespan_in_seconds


        
