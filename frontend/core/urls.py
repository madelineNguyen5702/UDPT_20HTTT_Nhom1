"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/employee/login/', LoginView.as_view(), name='login_view'),
    path('check_name/', check_name, name='check_name'),
    path('home/', getHome, name='getHome'),
    path('login/', getLogin, name='getLogin'),
    path('logout/', getLogout, name='getLogout'),
    # EMPLOYEE URL
    path('employee/home', getEmployeeHome, name='getEmployeeHome'),
    path('employee/activity', getEmployeeActivity, name='getEmployeeActivity'),
    path('employee/checkin', getEmployeeCheckIn, name='getEmployeeCheckIn'),
    path('employee/leave', getEmployeeLeave, name='getEmployeeLeave'),
    path('employee/points', getEmployeePoints, name='getEmployeePoints'),
    path('employee/profile', getEmployeeProfile, name='getEmployeeProfile'),
    path('employee/statusRequest', getEmployeesStatusRequest, name='getEmployeeStatusRequest'),
    path('employee/timesheet/viewDetail', getEmployeeViewTimesheetDetail, name='getEmployeeViewTimesheetDetail'),
    path('employee/timesheet/update', getEmployeeUpdateTimesheet, name='getEmployeeUpdateTimesheet'),
    path('employee/timesheet', getEmployeeViewTimesheet, name='getEmployeeViewTimesheet'),
    path('employee/voucher', getEmployeeVoucher, name='getEmployeeVoucher'),
    path('employee/wfh', getEmployeeWFH, name='getEmployeeWFH'),
    # MANAGER URL
    path('manager/home', getManagerHome, name='getManagerHome'),
    path('manager/viewList', getManagerViewList, name='getManagerViewList'),
    path('manager/givePoints', getManagerGivePoint, name='getManagerGivePoint'),
    path('manager/info', getManagerInfo, name='getManagerInfo'),
    path('manager/leave', getManagerLeave, name='getManagerLeave'),
    path('manager/requests', getManagerRequests, name='getManagerRequests'),
    path('manager/pointsList', getManagerPointsList, name='getManagerPointsList'),
    path('manager/updateTimesheet', getManagerUpdateTimesheet, name='getManagerUpdateTimesheet'),
    path('manager/viewList', getManagerViewList, name='getManagerViewList'),
    path('manager/wfh', getManagerWFH, name='getManagerWFH'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
