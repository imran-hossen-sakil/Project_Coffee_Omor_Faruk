"""
URL configuration for Coffee_Omor_Faruk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
# from views import *

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns




urlpatterns = [
    path("login/", views.login, name="login"),
    path("", views.admin_profile, name="admin_profile"),
    path("user/search/with/ajax/", views.user_search_with_ajax, name="user_search_with_ajax"),
    # path("user/versity/search/with/ajax/", views.user_versity_search_with_ajax, name="user_versity_search_with_ajax"),
    # path("Admin/Profile/", views.Admin_Profile, name="Admin_Profile"),
    path("daily/meal/entry/", views.daily_meal_entry, name="daily_meal_entry"),
    path("meal/feeding/entry/", views.meal_feeding_entry, name="meal_feeding_entry"),
    path("coffe/gave/to/student/", views.coffe_gave_to_student, name="coffe_gave_to_student"),
    path("user/list/", views.user_list, name="user_list"),
    path("user/edit/<str:id>/", views.user_edit, name="user_edit"),
    path("payment/receive/", views.payment, name="payment"),
    path("extra/food/bill/entry", views.extra_food, name="extra_food"),
    path("registration/", views.registration, name="registration"),
    path("last/meal/entry/time/", views.last_time_for_entry_meal, name="last_time_for_entry_meal"),
    path("update/meal/time/", views.meal_time_update, name="meal_time_update"),
    path("user/password/reset/", views.user_password_reset, name="user_password_reset"),
    path("daily/meal/report", views.date_wise_meal_report, name="date_wise_meal_report"),
    path("admins/logout/", views.admins_logout, name="admins_logout"),


    # path('meal/', meal.site.urls),
]


   