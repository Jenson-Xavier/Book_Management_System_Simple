"""
URL configuration for BMS project.

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
from django.conf.urls import *

import app.views

urlpatterns = [
    path('', app.views.login_view, name='main'),
    path('admin/', admin.site.urls),

    path('register_page/', app.views.register_view, name="register_page"),
    path('login_page/', app.views.login_view, name="login_page"),
    path('logout_page/', app.views.logout_view, name='logout_page'),
    path('register/', app.views.register, name='register'),
    path('login/', app.views.login, name='login'),

    path('staff_add_book/', app.views.staff_add_book, name='staff_add_book'),
    path('staff_alter_book/', app.views.staff_alter_book, name='staff_alter_book'),
    path('viewbook/', app.views.view_bookinfo, name='view_bookinfo'),
    path('index/', app.views.index_staff, name='index_staff'),

    path('staff_borrow_book/', app.views.staff_borrow_book, name='staff_borrow_book'),
    path('staff_return_book/', app.views.staff_return_book, name='staff_return_book'),
    path('staff_change_book_info/', app.views.staff_change_book_info, name='staff_change_book_info'),
    path('get_book_types/', app.views.get_book_types, name='get_book_types'),
    path('staff_view_user_info/', app.views.staff_view_user_info, name='staff_view_user_info'),
    path('staff_view_user/', app.views.staff_view_user, name='staff_view_user'),

    path('pressure_test/', app.views.pressure_test, name='pressure_test'),
]
