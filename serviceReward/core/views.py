from django.shortcuts import render
from rest_framework.views import APIView
from core.models import *  # Đảm bảo rằng bạn đã import đúng model
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.sessions.models import Session
from .serializers import *

class EmployeeVoucher(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getEmployeeVoucher')
    def getEmployeeVoucher(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = EmployeeVoucher.objects.filter(MaNV=manv)
            serializer = EmployeeVoucherSerializers(queryset, many=True)
            return Response(serializer.data)
        except EmployeeVoucherSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'], url_path='buyVoucher')
    def buyVoucher(self, request):
        manv = request.data.get('MaNV')
        mavoucher = request.data.get('MaVoucher')
        ngaymua = request.data.get('NgayMua')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request_update = EmployeeVoucher.objects.create(
                MaNV=manv,
                MaVoucher=mavoucher,
                NgayMua=ngaymua
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = EmployeeVoucherSerializers(request_update)

            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except EmployeeVoucherSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        

class EmployeePoint(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getEmployeePoint')
    def getEmployeePoint(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = NV_Point.objects.filter(MaNV=manv)
            serializer = NV_PointSerializers(queryset, many=True)
            return Response(serializer.data)
        except NV_PointSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'], url_path='updatePoint')
    def updatePoint(self, request):
        manv = request.data.get('MaNV')
        point = request.data.get('Point')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = NV_Point.objects.filter(MaNV=manv)
            # Cập nhật bản ghi
            num_updated = queryset.update(
                TongPoint= point
            )

            if num_updated == 0:
                return Response({'message': 'No records updated or found'}, status=status.HTTP_404_NOT_FOUND)

            # Tải lại queryset sau khi cập nhật
            updated_queryset = NV_Point.objects.filter(
                MaNV=manv
            )

            # Serialize lại dữ liệu sau khi cập nhật
            serializer = NV_PointSerializers(updated_queryset, many=True)

            # Trả về dữ liệu sau khi cập nhật
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NV_PointSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'], url_path='updateVoucher')
    def updateVoucher(self, request):
        manv = request.data.get('MaNV')
        point = request.data.get('Voucher')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = NV_Point.objects.filter(MaNV=manv)
            # Cập nhật bản ghi
            num_updated = queryset.update(
                TongVoucher= point
            )

            if num_updated == 0:
                return Response({'message': 'No records updated or found'}, status=status.HTTP_404_NOT_FOUND)

            # Tải lại queryset sau khi cập nhật
            updated_queryset = NV_Point.objects.filter(
                MaNV=manv
            )

            # Serialize lại dữ liệu sau khi cập nhật
            serializer = NV_PointSerializers(updated_queryset, many=True)

            # Trả về dữ liệu sau khi cập nhật
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NV_PointSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        

class PointLog(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getPointLog')
    def getPointLog(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = PointLog.objects.filter(MaNV=manv)
            serializer = PointLogSerializers(queryset, many=True)
            return Response(serializer.data)
        except PointLogSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'], url_path='managerSendPoint')
    def managerSendPoint(self, request):
        manv = request.data.get('MaNV')
        point = request.data.get('Point')
        nguoigui = request.data.get('NguoiGui')
        ngaycapnhat = request.data.get('NgayCapNhat')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request_update = PointLog.objects.create(
                MaNV=manv,
                Point=point,
                NguoiGui=nguoigui,
                Loai="Nhận",
                NgayCapNhat = ngaycapnhat
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = PointLogSerializers(request_update)

            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PointLogSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='employeeUsePoint')
    def employeeUsePoint(self, request):
        manv = request.data.get('MaNV')
        point = request.data.get('Point')
        ngaycapnhat = request.data.get('NgayCapNhat')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request_update = PointLog.objects.create(
                MaNV=manv,
                Point=point,
                Loai="Mua",
                NgayCapNhat = ngaycapnhat
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = PointLogSerializers(request_update)

            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PointLogSerializers.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        

class Voucher(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getVoucher')
    def getVoucher(self, request):
        try:
            queryset = Voucher.objects.all()
            serializer = VoucherSerializers(queryset, many=True)
            return Response(serializer.data)
        except VoucherSerializers.DoesNotExist:
            return Response({'error': 'No vouchers found'}, status=status.HTTP_404_NOT_FOUND)

