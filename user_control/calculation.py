from .models import *
from django.db.models import Avg, Count, Min, Sum, Max


class User_Calculation:
    def __init__(self, obj_user):
        self.user=obj_user
    
    def pay_book(self):
        total = self.user.payment_book_set.all().aggregate(Sum('amount'))['amount__sum']
        if total:
            return total
        else:
            return 0
    
    def food_bill(self):
        meals=self.user.student_meal_order_set.all()
        amount=0
        for meal in meals:
            amount += meal.quintity*meal.meal.amount
        if amount:
            return amount
        else:
            return 0

    def extra_food(self):
        total=self.user.extra_food_set.all().aggregate(Sum('amount'))['amount__sum']
        if total:
            return total
        else:
            return 0

    def final_calculation(self):
        return self.pay_book() - (self.food_bill()+self.extra_food())




    # def food_calculation(self):
        # pass
