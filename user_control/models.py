from django.db import models
from admin_control import models as acm
# Create your models here.

class Consumer_User(models.Model):
    user=models.OneToOneField(acm.Coffe_User, on_delete=models.CASCADE)
    versity_id=models.CharField(max_length=150, null=True, blank=True)

class Student_Meal_Order(models.Model):
    meal = models.ForeignKey(acm.Daily_Meal, on_delete=models.CASCADE)
    h_user = models.ForeignKey(Consumer_User, on_delete=models.CASCADE)
    date=models.DateField()# it would be manual entry always day +1
    # date=models.DateTimeField()# it would be manual entry always day +1
    time=models.TimeField(auto_now_add=True)
    quintity = models.PositiveIntegerField(default=1)
    received = models.BooleanField(default=False)


class Payment_Book(models.Model):
    c_user = models.ForeignKey(Consumer_User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    # payment_cagagory = models.ForeignKey(H_Payment_Catagory, on_delete=models.CASCADE)  # it will auto fillup
    # by program, not by manually
    amount = models.PositiveIntegerField()
    entry_by=models.ForeignKey(acm.Coffe_User, on_delete=models.CASCADE, null=True, blank=True)


class Extra_Food(models.Model):
    c_user = models.ForeignKey(Consumer_User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    detaild=models.TextField()
    amount=models.FloatField()
    entry_by = models.ForeignKey(acm.Coffe_User, on_delete=models.CASCADE)