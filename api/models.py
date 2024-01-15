from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    pass

    def change_password(self, new_password):
        self.password = make_password(new_password)
        self.save()

    def unactivate_user(self):
        self.is_active = False
        self.save()
        
    def activate_user(self):
        self.is_active = True
        self.save()
    
    def __str__(self) -> str:
        return self.username


class ResetPassword(models.Model):
    user = models.OneToOneField(CustomUser, related_name="reset", on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=256, blank=True, null=True)


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.CharField(max_length=32)
    person_age = models.SmallIntegerField()
    depart_date = models.DateField()
    returning_date = models.DateField()
    
    def __str__(self) -> str:
        return self.destination
