from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Coffe_User(AbstractUser):
    img = models.ImageField(upload_to="media/user/profile/", blank=True, null=True)
    phone_number=models.CharField(max_length=15, null=True, blank=True)


class Meal_Times(models.Model):
    meal_time = models.CharField(max_length=100)
    # meal feeding time range
    start_time=models.TimeField()
    end_time=models.TimeField()

class Daily_Meal(models.Model):
    meal_time = models.ForeignKey(Meal_Times, on_delete=models.CASCADE, null=True, blank=True)
    meal_name = models.CharField(max_length=400)
    date = models.DateField(auto_now=True)
    optional = models.BooleanField(default=False)  # if optional is false then it is main meal
    quintity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()  # each meal price
    entry_by=models.ForeignKey(Coffe_User, on_delete=models.CASCADE)

class End_Time_Of_Ordering_Meal(models.Model):
    time=models.TimeField()
