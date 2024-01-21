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
from django.contrib.auth import views as auth_views
from .views import *
# from Coffee_Omor_Faruk import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('meal/', meal.site.urls),
    # path("", views.index, name="home"),
    path("", views.user_profile, name="user_profile"),
    # path("admin/profile/", views.admin_profile, name="admin_profile"),
    path("user/meal/order/<str:id>/", views.user_meal_order, name="user_meal_order"),
    path("user/meal/order/remove/<str:id>/", views.user_meal_order_remove, name="user_meal_order_remove"),
    path("personal/meal/report/<str:id>/", views.personal_meal_report, name="personal_meal_report"),
    path("payment/statement/<str:id>/", views.payment_statement, name="payment_statement"),
    path("extra/food/histroy/<str:id>/", views.extar_food_history, name="extar_food_history"),
    # path("password/change/", auth_views.PasswordChangeView.as_view(template_name="password_change.html"), name="password_change"),
    # path("password/change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password/change/", views.password_change, name="password_change"),
    # path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name="test.html"), name='password_change_done'),
    path("user/logout/", views.user_logout, name="user_logout"),

    
]


