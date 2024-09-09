from django.shortcuts import render
from rest_framework.views import APIView
from core.models import *  # Đảm bảo rằng bạn đã import đúng model
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.sessions.models import Session
from .serializers import *

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
    @action(detail=False, methods=['get'], url_path='get_employees_by_manager')
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
 