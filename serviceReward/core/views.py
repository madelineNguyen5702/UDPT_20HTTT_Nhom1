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
    def get(self, request):
        data = request.data
        ma_nv = data.get('MaNV', '').strip()
        mat_khau = data.get('MatKhau', '').strip()
        if NhanVien.objects.filter(MaNV=ma_nv).exists():
            if NhanVien.objects.filter(MatKhau=mat_khau).exists():
                message = f"Authenticated"
            else:
                message = f"Mật khẩu không đúng"
        else:
            message = f"Tên '{ma_nv}' không tồn tại (not available)."

        return Response({'message': message}, status=status.HTTP_200_OK)
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
            message = f"Tên '{ma_nv}' không tồn tại (not available)."

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
        
class TimesheetView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getTimesheet')
    def getTimesheet(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = Timesheet.objects.filter(MaNV=manv)
            serializer = TimesheetSerializer(queryset, many=True)
            return Response(serializer.data)
        except Timesheet.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='getRequestUpdateTimesheet')
    def getRequestUpdateTimesheet(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = RequestUpdate.objects.filter(MaNV=manv)
            serializer = RequestUpdateSerializer(queryset, many=True)
            return Response(serializer.data)
        except RequestUpdate.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='requestUpdateTimesheet')
    def requestUpdateTimesheet(self, request):
        manv = request.data.get('MaNV')
        ngay = request.data.get('Ngay')
        checkin = request.data.get('Checkin')
        updatecheckin = request.data.get('updateCheckin')  # Thay đổi chỗ này
        checkout = request.data.get('Checkout')
        updatecheckout = request.data.get('updateCheckout')  # Thay đổi chỗ này
        ngaygui = request.data.get('NgayGui')
        chitiet = request.data.get('ChiTiet')
        trangthai = request.data.get('TrangThai')
        # ngayduyet = request.data.get('NgayDuyet')
        idnguoiduyet = request.data.get('IDNguoiDuyet')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            request_update = RequestUpdate.objects.create(
                MaNV=manv,
                Ngay=ngay,
                Checkin=checkin,
                updateCheckin=updatecheckin,
                Checkout=checkout,
                updateCheckout=updatecheckout,
                NgayGui=ngaygui,
                ChiTiet=chitiet,
                TrangThai=trangthai,
                # NgayDuyet=ngayduyet,
                IDNguoiDuyet=idnguoiduyet
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = RequestUpdateSerializer(request_update)

            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class LeaveView(viewsets.ViewSet):
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='getRequestLeave')
    def getRequestLeave(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = RequestLeave.objects.filter(MaNV=manv)
            serializer = RequestLeaveSerializer(queryset, many=True)
            return Response(serializer.data)
        except RequestLeave.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='requestLeave')
    def requestLeave(self, request):
        manv = request.data.get('MaNV')
        ngaygui = request.data.get('NgayGui')
        ngayrequest = request.data.get('NgayRequest')
        trangthai = request.data.get('TrangThai')
        idnguoiduyet = request.data.get('IDNguoiDuyet')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            request_update = RequestLeave.objects.create(
                MaNV=manv,
                NgayGui=ngaygui,
                NgayRequest=ngayrequest,
                TrangThai=trangthai,
                IDNguoiDuyet=idnguoiduyet
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = RequestLeaveSerializer(request_update)

            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='getRequestLeaveManager')
    def getRequestLeaveManager(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = RequestLeave.objects.filter(IDNguoiDuyet=manv, TrangThai="Chờ")
            serializer = RequestLeaveSerializer(queryset, many=True)
            return Response(serializer.data)
        except RequestLeave.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='handleRequestLeaveManager')
    def handleRequestLeaveManager(self, request):
        manv = request.data.get('MaNV')
        ngaygui = request.data.get('NgayGui')
        ngayrequest = request.data.get('NgayRequest')
        ngayduyet = request.data.get('NgayDuyet')
        trangthaimoi = request.data.get('TrangThai')
        idnguoiduyet = request.data.get('IDNguoiDuyet')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lọc bản ghi cần cập nhật
            queryset = RequestLeave.objects.filter(
                MaNV=manv,
                NgayGui=ngaygui,
                NgayRequest=ngayrequest,
                TrangThai="Chờ",
                IDNguoiDuyet=idnguoiduyet
            )

            if not queryset.exists():
                return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

            # Cập nhật bản ghi
            num_updated = queryset.update(
                NgayDuyet=ngayduyet,
                TrangThai=trangthaimoi
            )

            if num_updated == 0:
                return Response({'message': 'No records updated or found'}, status=status.HTTP_404_NOT_FOUND)

            # Tải lại queryset sau khi cập nhật
            updated_queryset = RequestLeave.objects.filter(
                MaNV=manv,
                NgayGui=ngaygui,
                NgayRequest=ngayrequest,
                TrangThai=trangthaimoi,
                IDNguoiDuyet=idnguoiduyet
            )

            # Serialize lại dữ liệu sau khi cập nhật
            serializer = RequestLeaveSerializer(updated_queryset, many=True)

            # Trả về dữ liệu sau khi cập nhật
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP)


class WFHView(viewsets.ViewSet):
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='getRequestWFH')
    def getRequestWFH(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = RequestWFH.objects.filter(MaNV=manv)
            serializer = RequestWFHSerializer(queryset, many=True)
            return Response(serializer.data)
        except RequestWFH.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='requestWFH')
    def requestWFH(self, request):
        manv = request.data.get('MaNV')
        ngaygui = request.data.get('NgayGui')
        ngayrequest = request.data.get('NgayRequest')
        trangthai = request.data.get('TrangThai')
        idnguoiduyet = request.data.get('IDNguoiDuyet')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            request_update = RequestWFH.objects.create(
                MaNV=manv,
                NgayGui=ngaygui,
                NgayRequest=ngayrequest,
                TrangThai=trangthai,
                IDNguoiDuyet=idnguoiduyet
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = RequestWFHSerializer(request_update)

            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='getRequestWFHManager')
    def getRequestWFHManager(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = RequestWFH.objects.filter(IDNguoiDuyet=manv, TrangThai="Chờ")
            serializer = RequestWFHSerializer(queryset, many=True)
            return Response(serializer.data)
        except RequestWFH.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='handleRequestWFHManager')
    def handleRequestWFHManager(self, request):
        manv = request.data.get('MaNV')
        ngaygui = request.data.get('NgayGui')
        ngayrequest = request.data.get('NgayRequest')
        ngayduyet = request.data.get('NgayDuyet')
        trangthaimoi = request.data.get('TrangThai')
        idnguoiduyet = request.data.get('IDNguoiDuyet')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lọc bản ghi cần cập nhật
            queryset = RequestWFH.objects.filter(
                MaNV=manv,
                NgayGui=ngaygui,
                NgayRequest=ngayrequest,
                TrangThai="Chờ"
            )

            if not queryset.exists():
                return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

            # Cập nhật bản ghi
            num_updated = queryset.update(
                NgayDuyet=ngayduyet,
                TrangThai=trangthaimoi
            )

            if num_updated == 0:
                return Response({'message': 'No records updated or found'}, status=status.HTTP_404_NOT_FOUND)

            # Tải lại queryset sau khi cập nhật
            updated_queryset = RequestWFH.objects.filter(
                MaNV=manv,
                NgayGui=ngaygui,
                NgayRequest=ngayrequest,
                TrangThai=trangthaimoi
            )

            # Serialize lại dữ liệu sau khi cập nhật
            serializer = RequestWFHSerializer(updated_queryset, many=True)

            # Trả về dữ liệu sau khi cập nhật
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP)