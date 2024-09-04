from django.shortcuts import render
from rest_framework.views import APIView
from core.models import NhanVien  # Đảm bảo rằng bạn đã import đúng model
import requests
class LoginView(APIView):
    def get(self, request):
        # Truy vấn tất cả các bản ghi từ bảng NhanVien
        nhanvien_list = NhanVien.objects.all()
        
        # Render template với dữ liệu
        context = {'nhanviens': nhanvien_list}
        return render(request, 'api.html', context)

def check_name(request):
    return render(request, 'check.html')

def getLogin(request):
    return render(request,'login.html')

def getHome(request):
    return render(request,'home.html')

def getLogout(request):
    return render(request, "logout.html")

# EMPLOYEE VIEW
def getEmployeeHome(request):
    return render(request,'employee/home.html')
def getEmployeeActivity(request):
    return render(request,'employee/activity.html')
def getEmployeeCheckIn(request):
    return render(request,'employee/checkIn.html')
def getEmployeeLeave(request):
    return render(request,'employee/leave.html')
def getEmployeePoints(request):
    return render(request,'employee/points.html')
def getEmployeeProfile(request):
    return render(request,'employee/profile.html')
def getEmployeesStatusRequest(request):
    return render(request,'employee/statusRequest.html')
def getEmployeeViewTimesheetDetail(request):
    return render(request,'employee/timesheet-viewDetail.html')
def getEmployeeUpdateTimesheet(request):
    return render(request,'employee/updateTimesheet.html')
def getEmployeeViewTimesheet(request):
    return render(request,'employee/viewTimeSheet.html')
def getEmployeeVoucher(request):
    return render(request,'employee/voucher.html')
def getEmployeeWFH(request):
    return render(request,'employee/wfh.html')


# MANAGER VIEW
def getManagerHome(request):
    return render(request,'manager/home.html')
def getManagerViewList(request):
    return render(request,'manager/viewList.html')
def getManagerGivePoint(request):
    return render(request,'manager/givePoints.html')
def getManagerInfo(request):
    return render(request,'manager/info.html')
def getManagerLeave(request):
    return render(request,'manager/leave.html')
def getManagerRequests(request):
    return render(request,'manager/requests.html')
def getManagerPointsList(request):
    return render(request,'manager/pointsList.html')
def getManagerUpdateTimesheet(request):
    return render(request,'manager/updateTimesheet.html')
def getManagerViewList(request):
    return render(request,'manager/viewList.html')
def getManagerWFH(request):
    return render(request,'manager/wfh.html')
