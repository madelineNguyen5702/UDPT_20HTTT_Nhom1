from django.shortcuts import render
from rest_framework.views import APIView
from core.models import *  # Đảm bảo rằng bạn đã import đúng model
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.sessions.models import Session
from .serializers import *
import requests

class LoginView(APIView):
    def get(self, request):
        # Truy vấn tất cả các bản ghi từ bảng NhanVien
        nhanvien_list = NhanVien.objects.all()
        
        # Render template với dữ liệu
        context = {'nhanviens': nhanvien_list}
        return render(request, 'api.html', context)

class CheckNhanVienView(APIView):
    # def get(self, request):
    #     data = request.data
    #     ma_nv = data.get('MaNV', '').strip()
    #     mat_khau = data.get('MatKhau', '').strip()

    #     # Kiểm tra dữ liệu có tồn tại trong cơ sở dữ liệu
    #     if NhanVien.objects.filter(MaNV=ma_nv).exists():
    #         if NhanVien.objects.filter(MatKhau=mat_khau).exists():
    #             message = f"Authenticated"
    #         else:
    #             message = f"Mật khẩu không đúng"
    #     else:
    #         message = f"Nhân viên '{ma_nv}' không tồn tại."

    #     return Response({'message': message}, status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data
        ma_nv = data.get('MaNV', '').strip()
        mat_khau = data.get('MatKhau', '').strip()

        # Kiểm tra dữ liệu có tồn tại trong cơ sở dữ liệu
        if NhanVien.objects.filter(MaNV=ma_nv).exists():
            if NhanVien.objects.filter(MatKhau=mat_khau).exists():
                message = f"Authenticated"
            else:
                message = f"Mật khẩu không đúng"
        else:
            message = f"Nhân viên '{ma_nv}' không tồn tại."

        return Response({'message': message}, status=status.HTTP_200_OK)
    
class DanhSachNhanVienQuanLyViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='get_employees_by_manager')
    def get_employees_by_manager(self, request):
        maql = request.data.get('MaQL')
        if not maql:
            return Response({'error': 'MaQL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = DanhSachNhanVienQuanLy.objects.filter(MaQL=maql)
            serializer = DanhSachNhanVienQuanLySerializer(queryset, many=True)
            return Response(serializer.data)
        except DanhSachNhanVienQuanLy.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeInfo(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getEmployeeInfo')
    def getEmployeeInfo(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = NhanVien.objects.filter(MaNV=manv)
            serializer = NhanVienSerializer(queryset, many=True)
            return Response(serializer.data)
        except NhanVien.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeActivity(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getEmployeeActivity')
    def getEmployeeActivity(self, request):
        ma_nv = request.data.get('MaNV')
        print(f"Received MaNV: {ma_nv}")  # Debugging: print MaNV to check if it's being received correctly
        if not ma_nv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Lấy thông tin từ bảng StravaCredentials
        try:
            credentials = HoatDongNhanVien.objects.get(MaNV=ma_nv)
            print(f"Retrieved token: {credentials.refresh_token}")  # Debugging: print token to check its value
        except HoatDongNhanVien.DoesNotExist:
            return Response({'error': 'Credentials not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Lấy access token từ refresh token
        try:
            access_token = credentials.access_token
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Gọi Strava API để lấy hoạt động
        url = "https://www.strava.com/api/v3/athlete/activities"
        headers = {
            "Authorization": f"Bearer {access_token}"  # Sử dụng access_token thay vì refresh_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return Response(data)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return Response({'error': f'HTTP error occurred: {http_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as req_err:
            print(f"Error occurred: {req_err}")
            return Response({'error': f'Error occurred: {req_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


