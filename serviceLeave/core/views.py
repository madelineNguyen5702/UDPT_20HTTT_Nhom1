from django.shortcuts import render
from rest_framework.views import APIView
from core.models import *  # Đảm bảo rằng bạn đã import đúng model
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.sessions.models import Session
from .serializers import *
from datetime import date
from datetime import datetime


class TimesheetView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='checkIn')
    def checkIn(self, request):
        print(request.data)
        manv = request.data.get('MaNV')
        ngay = request.data.get('Ngay')
        checkin = request.data.get('Checkin')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            request_update = Timesheet.objects.create(
                MaNV=manv,
                Ngay=ngay,
                Checkin=checkin
            )

            # Serialize dữ liệu của bản ghi mới
            serializer = TimesheetSerializer(request_update)
            print(serializer.data)
            # Trả về dữ liệu của bản ghi mới
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #------------------------------------------------------------------------    
    @action(detail=False, methods=['post'], url_path='checkOut')
    def checkOut(self, request):
        print(request.data)
        manv = request.data.get('MaNV')
        ngay = request.data.get('Ngay')
        checkout = request.data.get('Checkout')

        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lọc bản ghi cần cập nhật
            queryset = Timesheet.objects.filter(
                MaNV=manv,
                Ngay=ngay
            )

            if not queryset.exists():
                return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

            # Cập nhật bản ghi
            num_updated = queryset.update(
                Checkout = checkout
            )

            if num_updated == 0:
                return Response({'message': 'Không thể checkout'}, status=status.HTTP_404_NOT_FOUND)

            # Tải lại queryset sau khi cập nhật
            updated_queryset = Timesheet.objects.filter(
                MaNV=manv,
                Ngay=ngay,
            )

            # Serialize lại dữ liệu sau khi cập nhật
            serializer = TimesheetSerializer(updated_queryset, many=True)
            print(serializer.data)
            # Trả về dữ liệu sau khi cập nhật
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #------------------------------------------------------------------------  
    @action(detail=False, methods=['post'], url_path='getCheckIn')
    def getCheckIn(self, request):
        manv = request.data.get('MaNV')
        ngay = request.data.get('Ngay')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = Timesheet.objects.filter(MaNV=manv, Ngay=ngay)
            if(queryset.exists()): 
                serializer = TimesheetSerializer(queryset, many=True)
                print(serializer.data)
                return Response(serializer.data)
            else:
                message = "Not CheckIn"
                return Response({'message': message}, status=status.HTTP_200_OK)
            
        except Timesheet.DoesNotExist:
            return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
    #------------------------------------------------------------------------  
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
    @action(detail=False, methods=['post'], url_path='getRequestUpdateTimesheetManager')
    def getRequestUpdateTimesheetManager(self, request):
        manv = request.data.get('MaNV')
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = RequestUpdate.objects.filter(IDNguoiDuyet=manv, TrangThai="Chờ")
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
        
    #------------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path='handleRequestUpdateTimesheet')
    def handleRequestUpdateTimesheet(self, request):
        manv = request.data.get('MaNV')
        ngay = request.data.get('Ngay')
        checkin = request.data.get('Checkin')
        updatecheckin = request.data.get('updateCheckin')  # Thay đổi chỗ này
        checkout = request.data.get('Checkout')
        updatecheckout = request.data.get('updateCheckout')  # Thay đổi chỗ này
        trangthaimoi = request.data.get('TrangThai')
        idnguoiduyet = request.data.get('IDNguoiDuyet')
        if not manv or not ngay or not idnguoiduyet:
            return Response({'error': 'MaNV, Ngay, và IDNguoiDuyet là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

        # Format Ngay to only contain date part
        try:
            ngay = datetime.strptime(ngay.split('T')[0], '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Ngay không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

        # Set NgayDuyet to the current date
        ngayduyet = date.today().strftime('%Y-%m-%d')

        try:
            queryset = RequestUpdate.objects.filter(
                MaNV=manv,
                Ngay=ngay,
                IDNguoiDuyet=idnguoiduyet,
                TrangThai="Chờ"
            )

            if not queryset.exists():
                return Response({'error': 'Không có bảng ghi phù hợp'}, status=status.HTTP_404_NOT_FOUND)

            # Kiểm tra xem giá trị updateCheckin/updateCheckout có hợp lệ không
            if updatecheckin:
                try:
                    datetime.strptime(updatecheckin, '%H:%M')  # Kiểm tra định dạng HH:MM
                except ValueError:
                    return Response({'error': 'updateCheckin có định dạng không hợp lệ. Phải là HH:MM'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                updatecheckin = checkin  # Nếu không có giá trị mới, dùng giá trị cũ

            if updatecheckout:
                try:
                    datetime.strptime(updatecheckout, '%H:%M')  # Kiểm tra định dạng HH:MM
                except ValueError:
                    return Response({'error': 'updateCheckout có định dạng không hợp lệ. Phải là HH:MM'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                updatecheckout = checkout  # Nếu không có giá trị mới, dùng giá trị cũ

            # Cập nhật bản ghi RequestUpdate
            num_updated = queryset.update(
                TrangThai=trangthaimoi,
                NgayDuyet=ngayduyet,
            )

            if num_updated == 0:
                return Response({'message': 'Không có bản ghi nào được cập nhật'}, status=status.HTTP_404_NOT_FOUND)
            updated_data = RequestUpdate.objects.filter(MaNV=manv, Ngay=ngay)
            for i in updated_data:
                newCheckIn = i.updateCheckin
                newCheckOut = i.updateCheckout
            if trangthaimoi == 'Chấp thuận':
                try:
                    print("Update Timesheet")
                    # Cập nhật bản ghi Timesheet
                    querysett = Timesheet.objects.filter(MaNV=manv, Ngay=ngay)
                    num_updated = querysett.update(
                        Checkin=newCheckIn,
                        Checkout=newCheckOut
                    )

                    if num_updated == 0:
                        return Response({'message': 'Không có bản ghi nào được cập nhật trong Timesheet'}, status=status.HTTP_404_NOT_FOUND)

                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = RequestUpdateSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#--------------------------------------------------------------------------------------------------------------------------------------------

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
    # @action(detail=False, methods=['post'], url_path='handleRequestLeaveManager')
    # def handleRequestLeaveManager(self, request):
    #     manv = request.data.get('MaNV')
    #     ngaygui = request.data.get('NgayGui')
    #     ngayrequest = request.data.get('NgayRequest')
    #     ngayduyet = request.data.get('NgayDuyet')
    #     trangthaimoi = request.data.get('TrangThai')
    #     idnguoiduyet = request.data.get('IDNguoiDuyet')

    #     if not manv:
    #         return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Lọc bản ghi cần cập nhật
    #         queryset = RequestLeave.objects.filter(
    #             MaNV=manv,
    #             NgayGui=ngaygui,
    #             NgayRequest=ngayrequest,
    #             TrangThai="Chờ",
    #             IDNguoiDuyet=idnguoiduyet
    #         )

    #         if not queryset.exists():
    #             return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

    #         # Cập nhật bản ghi
    #         num_updated = queryset.update(
    #             NgayDuyet=ngayduyet,
    #             TrangThai=trangthaimoi
    #         )

    #         if num_updated == 0:
    #             return Response({'message': 'No records updated or found'}, status=status.HTTP_404_NOT_FOUND)

    #         # Tải lại queryset sau khi cập nhật
    #         updated_queryset = RequestLeave.objects.filter(
    #             MaNV=manv,
    #             NgayGui=ngaygui,
    #             NgayRequest=ngayrequest,
    #             TrangThai=trangthaimoi,
    #             IDNguoiDuyet=idnguoiduyet
    #         )

    #         # Serialize lại dữ liệu sau khi cập nhật
    #         serializer = RequestLeaveSerializer(updated_queryset, many=True)

    #         # Trả về dữ liệu sau khi cập nhật
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP)


    @action(detail=False, methods=['post'], url_path='handleRequestLeaveManager')

    def handleRequestLeaveManager(self, request):
        manv = request.data.get('MaNV')
        ngayrequest = request.data.get('NgayRequest')  # Added to filter the correct record
        idnguoiduyet = request.data.get('IDNguoiDuyet')  # Ensure this is the correct field name
        trangthaimoi = request.data.get('TrangThai')

        if not manv or not ngayrequest or not idnguoiduyet:
            return Response({'error': 'MaNV, NgayRequest, và IDNguoiDuyet là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

        # # Set NgayDuyet to the current date
        # ngayduyet = date.today().strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD

        # Format NgayRequest to only contain date part
        try:
            ngayrequest = datetime.strptime(ngayrequest.split('T')[0], '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'NgayRequest không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

        # Set NgayDuyet to the current date
        ngayduyet = date.today().strftime('%Y-%m-%d')


        try:
            # Filter using the correct field names
            queryset = RequestLeave.objects.filter(
                MaNV=manv,
                NgayRequest=ngayrequest,
                IDNguoiDuyet=idnguoiduyet,
                TrangThai="Chờ"
            )

            if not queryset.exists():
                return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

            # Update the record
            num_updated = queryset.update(
                NgayDuyet=ngayduyet,
                TrangThai=trangthaimoi
            )

            if num_updated == 0:
                return Response({'message': 'Không có bản ghi nào được cập nhật'}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the updated records
            updated_queryset = RequestLeave.objects.filter(
                MaNV=manv,
                NgayRequest=ngayrequest,
                IDNguoiDuyet=idnguoiduyet
            )

            serializer = RequestLeaveSerializer(updated_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#--------------------------------------------------------------------------------------------------------------------------------------------

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
    # @action(detail=False, methods=['post'], url_path='handleRequestWFHManager')
    # def handleRequestWFHManager(self, request):
    #     manv = request.data.get('MaNV')
    #     ngaygui = request.data.get('NgayGui')
    #     ngayrequest = request.data.get('NgayRequest')
    #     ngayduyet = request.data.get('NgayDuyet')
    #     trangthaimoi = request.data.get('TrangThai')

    #     if not manv:
    #         return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Lọc bản ghi cần cập nhật
    #         queryset = RequestWFH.objects.filter(
    #             MaNV=manv,
    #             NgayGui=ngaygui,
    #             NgayRequest=ngayrequest,
    #             TrangThai="Chờ"
    #         )

    #         if not queryset.exists():
    #             return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

    #         # Cập nhật bản ghi
    #         num_updated = queryset.update(
    #             NgayDuyet=ngayduyet,
    #             TrangThai=trangthaimoi
    #         )

    #         if num_updated == 0:
    #             return Response({'message': 'No records updated or found'}, status=status.HTTP_404_NOT_FOUND)

    #         # Tải lại queryset sau khi cập nhật
    #         updated_queryset = RequestWFH.objects.filter(
    #             MaNV=manv,
    #             NgayGui=ngaygui,
    #             NgayRequest=ngayrequest,
    #             TrangThai=trangthaimoi
    #         )

    #         # Serialize lại dữ liệu sau khi cập nhật
    #         serializer = RequestWFHSerializer(updated_queryset, many=True)

    #         # Trả về dữ liệu sau khi cập nhật
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP)

    @action(detail=False, methods=['post'], url_path='handleRequestWFHManager')
    def handleRequestWFHManager(self, request):
        manv = request.data.get('MaNV')
        ngayrequest = request.data.get('NgayRequest')  # Added to filter the correct record
        idnguoiduyet = request.data.get('IDNguoiDuyet')  # Ensure this is the correct field name
        trangthaimoi = request.data.get('TrangThai')

        if not manv or not ngayrequest or not idnguoiduyet:
            return Response({'error': 'MaNV, NgayRequest, và IDNguoiDuyet là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

        # # Set NgayDuyet to the current date
        # ngayduyet = date.today().strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD

        # Format NgayRequest to only contain date part
        try:
            ngayrequest = datetime.strptime(ngayrequest.split('T')[0], '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'NgayRequest không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

        # Set NgayDuyet to the current date
        ngayduyet = date.today().strftime('%Y-%m-%d')


        try:
            # Filter using the correct field names
            queryset = RequestWFH.objects.filter(
                MaNV=manv,
                NgayRequest=ngayrequest,
                IDNguoiDuyet=idnguoiduyet,
                TrangThai="Chờ"
            )

            if not queryset.exists():
                return Response({'error': 'Không có yêu cầu phù hợp'}, status=status.HTTP_404_NOT_FOUND)

            # Update the record
            num_updated = queryset.update(
                NgayDuyet=ngayduyet,
                TrangThai=trangthaimoi
            )

            if num_updated == 0:
                return Response({'message': 'Không có bản ghi nào được cập nhật'}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the updated records
            updated_queryset = RequestWFH.objects.filter(
                MaNV=manv,
                NgayRequest=ngayrequest,
                IDNguoiDuyet=idnguoiduyet
            )

            serializer = RequestWFHSerializer(updated_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)