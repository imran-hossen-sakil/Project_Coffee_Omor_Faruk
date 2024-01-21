from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from admin_control.models import *
from user_control.models import *
from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum, Max
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.contrib import auth 
from django.contrib import admin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission, PermissionManager #permission_required
from user_control import views
# @permission_required('is_superuser')

from user_control import models
from user_control import urls
from user_control.views import user_profile
from django.contrib.auth.decorators import login_required
from user_control.calculation import *
# Create your views here.

def login(request):
    context = {}
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        if request.method=="POST":
            user=auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                if request.user.is_superuser:
                    return redirect('admin_profile')
                else:
                    return redirect('user_profile')
            else:
                return render(request, "login.html", {'error_message': "Invalid Email or Password"})
    except Exception as e:
        context['error_message'] = str(e)
    return render(request,"login.html", context)


@permission_required('is_superuser')
@login_required(login_url='login')
def admin_profile(request):
    meal_tim = Meal_Times.objects.all().order_by('id')
    daily_meal_time_report = {}
    for mt in meal_tim:
        daily_meal_time_report[mt] = {}
    context = {
        'meal_tim':meal_tim,
        'daily_meal_time_report':daily_meal_time_report
    }
    return render(request, "admin_profile.html", context)

@permission_required('is_superuser')
@login_required(login_url='login')
def user_search_with_ajax(request):
    user_id = request.POST.get('user_id', None)
    obj_cu=Coffe_User.objects.filter(Q(phone_number=user_id) | Q(username= user_id))
    obj_con_u=Consumer_User.objects.filter(Q(user__phone_number=user_id) | Q(user__username= user_id))
    context={
        'obj_user': list(obj_cu.values()),
        'obj_users': list(obj_con_u.values()),
    }
    return JsonResponse(context)

@permission_required('is_superuser')
@login_required(login_url='login')
def daily_meal_entry(request):
    all_meal_times = Meal_Times.objects.all().order_by('id')
    counter=[x for x in range(1,21)]
    context = {
        'meal_time':all_meal_times,
        'counter':counter
    }
    if request.method == "POST":
        for c in counter:
            meal_price = request.POST.get(f'meal_price{c}')
            if not meal_price:
                continue
            try:
                meal_times = request.POST.get(f'meal_times{c}')
                meal_name = request.POST.get(f'meal_name{c}')
                meal_quantity = request.POST.get(f'meal_quantity{c}')
                optionals = request.POST.get(f'optionals{c}')
                Daily_Meal.objects.create(meal_time_id=meal_times,
                                    meal_name=meal_name,
                                    quintity=meal_quantity,
                                    amount=meal_price,
                                    entry_by=request.user,
                                    optional=True if bool(optionals) else False)
            except Exception as e:
                context['error_message'] = str(e)
                break
        return render(request, "daily_meal_entry.html", context)
    return render(request, "daily_meal_entry.html", context)

@permission_required('is_superuser')
@login_required(login_url='login')
def meal_feeding_entry(request):
    meal_tim=Meal_Times.objects.all().order_by('id')

    coffe_wise_meal = Student_Meal_Order.objects.filter(date=datetime.now().date()+timedelta(days=1))

    coffe_wise_meal_userid_only = coffe_wise_meal.values_list('h_user__id', flat=True).distinct()[:2]
    meal_sheet_report = {}
    for huid in coffe_wise_meal_userid_only:
        obj_coffe_user = Consumer_User.objects.get(id=huid)
        meal_sheet_report[obj_coffe_user] = {}
        for mt in meal_tim:
            meal_sheet_report[obj_coffe_user][mt] = coffe_wise_meal.filter(h_user__id=huid,
                                                                             meal__meal_time__id=mt.id)
    context={
        'search_date':datetime.now().date(),
        'meal_tim': meal_tim,
        'coffe_wise_meal':meal_sheet_report
    }
    try:
        if request.method=='POST':
            fodate=request.POST.get('fodate')
            # obj_date=datetime.strptime(fodate, '%Y-%m-%d').date()
            # obj_date_p_one_day=obj_date+timedelta(days=1)
            search_id=request.POST.get('search_id')
            error_message = "The Information You Provided Is Incorrect." 
            if fodate:
                coffe_wise_meal = Student_Meal_Order.objects.filter(date=fodate)
                if coffe_wise_meal:  
                    error_message = ""
            elif search_id:
                coffe_wise_meal=coffe_wise_meal.filter(Q(h_user__user__username=search_id)| Q(h_user__user__phone_number=search_id))
                if coffe_wise_meal:  
                    error_message = ""
            
            time_wise_meal_userid_only = coffe_wise_meal.values_list('h_user__id', flat=True).distinct()
            meal_sheet_report = {}
            for huid in time_wise_meal_userid_only:
                obj_coffe_user = Consumer_User.objects.get(id=huid)
                meal_sheet_report[obj_coffe_user] = {}
                for mt in meal_tim:
                    meal_sheet_report[obj_coffe_user][mt] = coffe_wise_meal.filter(h_user__id=huid,
                                                                                    meal__meal_time__id=mt.id)
            context['search_date']=fodate
            context['coffe_wise_meal']=meal_sheet_report
            context['error_message']=error_message
            return render(request, 'meal_feeding_entry.html', context)
    except Exception as e:
        context['error_message'] = str(e)
    return render(request, 'meal_feeding_entry.html', context)


@permission_required('is_superuser')
@login_required(login_url='login')
def coffe_gave_to_student(request):# hostel user profile and studnet meal order table id and dining table id
    coffe_user = request.POST.get('coffe_user', None)
    coffe_meal_time = request.POST.get('coffe_meal_time', None)
    Student_Meal_Order.objects.filter(h_user__id=coffe_user,
                                    meal__meal_time__id=coffe_meal_time
                                    ).update(received=True)
    return redirect(meal_feeding_entry)

@permission_required('is_superuser')
@login_required(login_url='login')
def user_list(request):
    cofe_users = Consumer_User.objects.all().order_by('id') 
    users={}
    for cof_user in cofe_users:
        users[cof_user]=User_Calculation(cof_user)
    context = {
        'cofe_users':users,
    }
    try:
        if request.method == "POST":
            search_id = request.POST.get('search_id')
            cofe_users = cofe_users.filter(Q(user__phone_number=search_id) | Q(user__username=search_id))
            users = {}
            for cof_user in cofe_users:
                users[cof_user] = User_Calculation(cof_user)
            context = {
                'cofe_users':users,
            }
            return render(request, "user_list.html", context)
    except Exception as e:
        context['error_message'] = str(e)
    return render(request, "user_list.html", context)

@permission_required('is_superuser')
@login_required(login_url='login')
def user_edit(request, id):
    cofe_users = Consumer_User.objects.get(id=id)
    obj_user=cofe_users.user

    context = {
        'cofe_users':cofe_users
    }

    if request.method == "POST":
        try:
            user_photo = request.FILES.get('user_photo')
            if user_photo:
                obj_user.img=user_photo
            first_name = request.POST.get('first_name')
            obj_user.first_name=first_name
            last_name = request.POST.get('last_name')
            obj_user.last_name=last_name
            phone_number = request.POST.get('phone_number')
            obj_user.phone_number=phone_number
            versity_id = request.POST.get('versity_id')
            if versity_id:
                cofe_users.obj_Consr_user=versity_id
                cofe_users.save()
            email = request.POST.get('email')
            obj_user.email=email

            inactive = request.POST.get('inactive')
            obj_user.is_active= False if inactive else True

            obj_user.save()



            context = {'successfull': 'Successfully'}



            return redirect(user_list)
            # return render(request, 'user_edit.html', context)

        except Exception as e:
            context['error_message'] = str(e)

    return render(request, "user_edit.html", context)

@permission_required('is_superuser')
@login_required(login_url='login')
def payment(request):
    context = {}
    try:
        if request.method == "POST":
            versity = request.POST.get('versity')
            user_name = request.POST.get('user_name')
            emails = request.POST.get('emails')
            amounts = request.POST.get('amounts')
            if versity:
                cons_user = Consumer_User.objects.get(versity_id=versity,
                                                    user__username=user_name,
                                                    user__email=emails)
                
            else:
                cons_user = Consumer_User.objects.get(user__username=user_name,
                                                      user__email=emails)
            Payment_Book.objects.create(c_user=cons_user,
                                        amount=amounts,
                                        entry_by=request.user)
            context = {'successfull': 'Successfully payment Entry Done'}
    except Exception as e:
        context = {'error_message': str(e)}
    return render(request, "payment.html", context)

@permission_required('is_superuser')
@login_required(login_url='login')
def extra_food(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        details = request.POST.get('details')
        amounts = request.POST.get('amounts')
        try:
            obj_user = Consumer_User.objects.get(user__username=user_id)
            obj_user.extra_food_set.create(
                detaild=details,
                amount=amounts,
                entry_by=request.user
            )
            context = {'successfull': 'Successfully payment Entry Done'}
            return render(request, "extra_food.html", context)
        except Exception as e:
            context = {'error_message': str(e)}
            return render(request, "extra_food.html", context)
    return render(request, "extra_food.html")

@permission_required('is_superuser')
@login_required(login_url='login')
def registration(request):
    current_user_list = Consumer_User.objects.all().count()
    final_user_id=f'C-0{current_user_list+1}'
    context = {
        'user_id':final_user_id
    }
    try:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            user_photo = request.FILES.get('user_photo')
            email = request.POST.get('email')
            password = request.POST.get('password')
            conform_pasword = request.POST.get('conform_pasword')
            if password == conform_pasword:
                user_create = Coffe_User(first_name=first_name,last_name=last_name,
                                    phone_number=phone_number,img=user_photo,
                                    username=final_user_id,email=email,
                                    )
                user_create.set_password(password)
                user_create.save()

                versity_id = request.POST.get('versity_id')
                if versity_id:
                    Consumer_User.objects.create(user=user_create,
                                                 versity_id=versity_id)
                else:
                    Consumer_User.objects.create(user=user_create)
                context = {'successfull': 'Successfully Registration Done'}
                return render(request, "registration.html", context)
            else:
                context = {'error_message': 'Passwords Do Not Match Please Try Againe'}
                return render(request, "registration.html", context)
    except Exception as e:
        context['error_message'] = str(e)
    return render(request, "registration.html", context)

@permission_required('is_superuser')
@login_required(login_url='login')
def meal_time_update(request):
    if request.method=='POST':
        meal_time_id=request.POST.get('meal_time_id')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        obj_mt=Meal_Times.objects.get(id=meal_time_id)
        obj_mt.start_time=start_date
        obj_mt.end_time=end_date
        obj_mt.save()
    return redirect(admin_profile)



@permission_required('is_superuser')
@login_required(login_url='login')
def last_time_for_entry_meal(request):
    if request.method=='POST':
        time=request.POST.get('times')
        obj_end_time=End_Time_Of_Ordering_Meal.objects.last()
        obj_end_time.time=time
        obj_end_time.save()
    return redirect(admin_profile)



@permission_required('is_superuser')
@login_required(login_url='login')
def user_password_reset(request):
    if request.method=='POST':
        user_id=request.POST.get('user_id')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password == confirm_password:
            obj_cu=Coffe_User.objects.get(username=user_id)
            obj_cu.set_password(confirm_password)
            obj_cu.save()
    return render(request, 'password_reset.html')



@permission_required('is_superuser')
@login_required(login_url='login')
def date_wise_meal_report(request):
    mts=Meal_Times.objects.all()
    output={}
    for mt in mts:
        output[mt]={}
        meals=mt.daily_meal_set.filter(date=datetime.now().date())# with time
        for meal in meals:
            output[mt][meal]={}
            orders_count=meal.student_meal_order_set.all().aggregate(Sum('quintity'))['quintity__sum']
            feeded_count=meal.student_meal_order_set.filter(received=True).aggregate(Sum('quintity'))['quintity__sum']
            output[mt][meal]['order_count']=orders_count
            output[mt][meal]['feeded_count']=feeded_count if feeded_count else 0


    context={
        'meals':output
    }
    if request.method=='POST':
        date=request.POST.get('date')
        output[mt]={}
        meals=mt.daily_meal_set.filter(date=date)# with time
        for meal in meals:
            output[mt][meal]={}
            orders_count=meal.student_meal_order_set.all().aggregate(Sum('quintity'))['quintity__sum']
            feeded_count=meal.student_meal_order_set.filter(received=True).aggregate(Sum('quintity'))['quintity__sum']
            output[mt][meal]['order_count']=orders_count
            output[mt][meal]['feeded_count']=feeded_count if feeded_count else 0

        return render(request, 'daliy_meal_order_report.html', context)
    return render(request, 'daliy_meal_order_report.html', context)


@login_required(login_url='login')
def admins_logout(request):
    auth.logout(request)
    return redirect(login)
