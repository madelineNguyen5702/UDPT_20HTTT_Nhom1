from django.shortcuts import render
from rest_framework.views import APIView
from core.models import NhanVien  # Đảm bảo rằng bạn đã import đúng model
from rest_framework.response import Response
from rest_framework import status
class LoginView(APIView):
    def get(self, request):
        # Truy vấn tất cả các bản ghi từ bảng NhanVien
        nhanvien_list = NhanVien.objects.all()
        
        # Render template với dữ liệu
        context = {'nhanviens': nhanvien_list}
        return render(request, 'api.html', context)

class CheckNhanVienView(APIView):
    def get(self, request):
        name = request.data.get('name')
        exists = NhanVien.objects.filter(name=name).exists()
        if NhanVien.objects.filter(name=name).exists():
            message = f"Tên '{name}' có sẵn (available)."
        else:
            message = f"Tên '{name}' không tồn tại (not available)."
        return Response({'message': message}, status=status.HTTP_200_OK)
    def post(self, request):
        name = request.data.get('name')
        exists = NhanVien.objects.filter(name=name).exists()
        if NhanVien.objects.filter(name=name).exists():
            message = f"Tên '{name}' có sẵn (available)."
        else:
            message = f"Tên '{name}' không tồn tại (not available)."
        return Response({'message': message}, status=status.HTTP_200_OK)