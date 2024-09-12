from pymongo import MongoClient
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from bson import ObjectId

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['UDPT'] 
collection = db['EmployeePoint'] 

class EmployeePoint(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='getEmployeePoint')
    def getEmployeePointInfo(self, request):
        # Lấy MaNV từ request
        manv = request.data.get('MaNV')

        # Kiểm tra nếu không có MaNV trong request
        if not manv:
            return Response({'error': 'MaNV is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Tìm kiếm nhân viên theo MaNV trong MongoDB
            employee = collection.find_one({"MaNV": manv})

            # Nếu không tìm thấy nhân viên
            if not employee:
                return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

            # Chuẩn bị dữ liệu để trả về
            response_data = {
                'MaNV': employee.get('MaNV'),
                'HoTen': employee.get('HoTen'),
                'CurrentPoint': employee.get('CurrentPoint'),
                'PointHistory': employee.get('PointHistory', [])  # Lấy lịch sử point nếu có
            }

            # Trả về dữ liệu JSON
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

