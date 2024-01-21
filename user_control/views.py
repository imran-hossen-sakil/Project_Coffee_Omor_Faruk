from django.shortcuts import render,redirect
from Coffee_Omor_Faruk import *
from admin_control.models import *
from datetime import datetime, timedelta
from user_control.models import *
from django.db.models import Avg, Count, Min, Sum, Max
from django.db import IntegrityError
from datetime import datetime
from django.contrib import auth 
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission, PermissionManager
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q, F
from .calculation import *
from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.

def str_to_date(date):
    return datetime.strptime(date,'%Y-%m-%d').date()

@login_required(login_url='login')
def user_profile(request):
    if request.user.is_superuser:
        return redirect('/acontrol')

    consum_user = request.user.consumer_user
    meal_order_last_time=acm.End_Time_Of_Ordering_Meal.objects.last()  #End_Time_Of_Ordering_Meal
    cal=User_Calculation(consum_user)
    daily_meal = acm.Daily_Meal.objects.filter(date=datetime.now().date()).order_by('id')
    date_with_one_addition = datetime.now().date()+timedelta(days=1)

    last_days_meals = Student_Meal_Order.objects.filter(h_user=consum_user,
                                                        date=date_with_one_addition).order_by('meal__meal_time__id')

    daily_meal_for_front = {}
    for meal in daily_meal:
        daily_meal_for_front[meal] = {}
        ordered_meal = meal.student_meal_order_set.all().aggregate(Sum('quintity'))['quintity__sum']
        if bool(ordered_meal):
            ordered_meal = ordered_meal
        else:
            ordered_meal = 0
        available_meal = meal.quintity - ordered_meal
        daily_meal_for_front[meal]['available'] = available_meal
    meal_times = Meal_Times.objects.all().order_by('id')

    context = {
        'daily_meals': daily_meal_for_front,
        'meal_times': meal_times,
        'last_days_meals': last_days_meals,
        'consum_user':consum_user,
        'cal':cal,
        'meal_order_last_time':meal_order_last_time

    }
    return render(request, "user_profile.html", context)

   

@login_required(login_url='login')
def user_meal_order(request, id): # Daily meal table id/ pk
    obj_daily_meal=acm.Daily_Meal.objects.get(id=id)

    user = Consumer_User.objects.get(user=request.user)
    ucal=User_Calculation(user)
    ordered_meal=obj_daily_meal.student_meal_order_set.all().aggregate(Sum('quintity'))['quintity__sum']
    if bool(ordered_meal):
        ordered_meal = ordered_meal
    else:
        ordered_meal = 0
    avileable_meal=obj_daily_meal.quintity - ordered_meal
    quintity=request.POST.get('quintity')
    obj_meal_order_time=acm.End_Time_Of_Ordering_Meal.objects.last()
    date_with_one_addition=datetime.now()+timedelta(days=1)
    meal_price=obj_daily_meal.amount*int(quintity)
    balance=ucal.final_calculation()
    if meal_price>balance:
        return redirect(user_profile)

    if datetime.now().time() < obj_meal_order_time.time: # time check
        if quintity is not None and int(quintity) > avileable_meal:
            return redirect(user_profile)
        try:
            check=Student_Meal_Order.objects.get(meal=obj_daily_meal, h_user=user,
                                                 date=date_with_one_addition.date())
            check.quintity = check.quintity + int(quintity)
            check.save()
            print(check)
        except:
            if obj_daily_meal.optional:
                check_main_meal= Student_Meal_Order.objects.filter(h_user=user, date=date_with_one_addition,
                                                                   meal__meal_time__id=obj_daily_meal.meal_time.id,
                                                                   meal__optional=False)# if optional is false meaning it main meal

                if check_main_meal:
                    new = Student_Meal_Order(meal=obj_daily_meal, h_user=user,
                                             quintity=quintity,
                                             date=date_with_one_addition)
                    new.save()

            else:
                new = Student_Meal_Order(meal=obj_daily_meal, h_user=user,
                                         quintity=quintity,
                                         date=date_with_one_addition)
                new.save()

    return redirect(user_profile)

@login_required(login_url='login')
def user_meal_order_remove(request, id):  # Student Meal Order tabile id/ pk
    obj_meal_order_time = acm.End_Time_Of_Ordering_Meal.objects.last()
    if not datetime.now().time() < obj_meal_order_time.time:
        return redirect(user_profile)

    obj_meal_order=Student_Meal_Order.objects.get(id=id)
    if not obj_meal_order.meal.optional:
        check_optional=Student_Meal_Order.objects.filter(h_user=obj_meal_order.h_user,
                                                         date=obj_meal_order.date,
                                                         meal__meal_time__id=obj_meal_order.meal.meal_time.id,
                                                         meal__optional=True)
        if obj_meal_order.quintity > 1:
            obj_meal_order.quintity=obj_meal_order.quintity-1
            obj_meal_order.save()

        elif not(check_optional):
            obj_meal_order.delete()

    else:
        if obj_meal_order.quintity > 1:
            obj_meal_order.quintity=obj_meal_order.quintity-1
            obj_meal_order.save()
        else:
            obj_meal_order.delete()
    return redirect(user_profile)

@login_required(login_url='login')
def personal_meal_report(request, id):
    consum_user=Consumer_User.objects.get(id=id)
    meal_tim=Meal_Times.objects.all()
    from_date=datetime.strptime(f'{datetime.now().year}-{datetime.now().month}-01'
                                ,'%Y-%m-%d').date()
    to_date=datetime.now().date()
    personal_user_meal_report={}
    while from_date<=to_date:
        personal_user_meal_report[from_date]={}
        for mt in meal_tim:
            personal_user_meal_report[from_date][mt]={}
            meal=Student_Meal_Order.objects.filter(
                h_user__id=consum_user.id,
                date=from_date,
                meal__meal_time__id=mt.id,
            )
            personal_user_meal_report[from_date][mt]=meal
        from_date +=timedelta(days=1)

    context={
        'meals':personal_user_meal_report,
        'meal_tim':meal_tim,
        'consum_user':consum_user
    }
    # return render(request, "personal_meal_report.html", context)

    if request.method=='POST':
        fodate=request.POST.get('fodate')
        todate=request.POST.get('todate')
        ssingla_user_meal_hestory={}
        if fodate and todate:
            fdate,tdate= str_to_date(fodate),str_to_date(todate)
        elif fodate:
            fdate, tdate= str_to_date(fodate),datetime.now().date()
        else:
            fdate, tdate = str_to_date(fodate), datetime.now().date()

        while fdate <= tdate:
            personal_user_meal_report[fdate] = {}
            for mt in meal_tim:
                personal_user_meal_report[fdate][mt] = {}
                meal = Student_Meal_Order.objects.filter(
                    h_user__id=consum_user.id,
                    date=fdate,
                    meal__meal_time__id=mt.id,
                )
                personal_user_meal_report[fdate][mt] = meal
            fdate += timedelta(days=1)
        return render(request, "personal_meal_report.html", context)
    return render(request, "personal_meal_report.html", context)

@login_required(login_url='login')
def payment_statement(request, id): # bring id
    cofe_user= Consumer_User.objects.get(id=id)
    pay_bok = cofe_user.payment_book_set.all()

    context = {
        "pay_bok":pay_bok,
        'cofe_user':cofe_user,
        # 'consum_user':consum_user
    }
    try:
        if request.method == 'POST':
            fodate = request.POST.get('fodate')
            todate = request.POST.get('todate')
            error_message = "The Information You Provided Is Incorrect." 
            if fodate and todate:
                pay_bok = pay_bok.filter(date__range=[str_to_date(fodate),
                                                    str_to_date(todate)])
                if pay_bok:  
                    error_message = ""
            elif fodate:
                pay_bok = pay_bok.ilter(date__range=[str_to_date(fodate),
                                                                    datetime.now().date()])
                if pay_bok:  
                    error_message = ""
            elif todate:
                pay_bok = pay_bok.filter(date=str_to_date(todate))
                if pay_bok:  
                    error_message = ""
  
            context['pay_bok']=pay_bok
            context['cofe_user']=cofe_user
            context['error_message']=error_message
            return render(request, "payment_statement.html", context)
    except Exception as e:
        context['error_message']= str(e)
    return render(request, "payment_statement.html", context)

@login_required(login_url='login')
def extar_food_history(request, id):
    cofe_user = Consumer_User.objects.get(id=id)
    extra_foods = cofe_user.extra_food_set.all()
    context = {
        "extra_foods": extra_foods,
        'cofe_user': cofe_user,
    }
    if request.method == 'POST':
        fodate = request.POST.get('fodate')
        todate = request.POST.get('todate')
        error_message = "The Information You Provided Is Incorrect."

        if fodate and todate:
            extra_foods = extra_foods.filter(date__range=[str_to_date(fodate),
                                                               str_to_date(todate)])
            if extra_foods:
                error_message = ""
        elif fodate:
            extra_foods = extra_foods.filter(date__range=[str_to_date(fodate),
                                                               datetime.now().date()])
            if extra_foods:
                error_message = ""
        elif todate:
            extra_foods = extra_foods.filter(date=str_to_date(todate))
            if extra_foods:
                error_message = ""

        context['extra_foods'] = extra_foods
        context['cofe_user'] = cofe_user
        context['error_message'] = error_message
        return render(request, "extra_food_histroy.html", context)

    return render(request, 'extra_food_histroy.html',context)



@login_required(login_url='login')
def password_change(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        conform_password = request.POST.get('conform_password')
        obj_user=request.user
        # print(current_password, new_password, conform_password, request.user.username)
        # # try:
        # user = auth.authenticate(username=request.user.username, password=current_password)
        # print(user)
        # if user is not None:# and new_password==conform_password:
        obj_user.set_password(new_password)
        obj_user.save()
            # print('here it is working')
        # except Exception as e:
        #     print('i am not working')
        #     pass

    return render(request, "password_change.html",)




@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    return redirect('/')