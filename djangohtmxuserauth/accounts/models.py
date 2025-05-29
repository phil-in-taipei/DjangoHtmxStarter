from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    
    def __str__(self):
        return f"{self.given_name} {self.surname}"
