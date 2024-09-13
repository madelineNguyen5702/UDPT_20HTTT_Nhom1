from rest_framework import serializers
from .models import *

class NhanVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhanVien
        fields = '__all__'

class DanhSachNhanVienQuanLySerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhSachNhanVienQuanLy
        fields = '__all__'
        

class HoatDongNhanVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoatDongNhanVien
        fields = '__all__'

# class TimesheetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Timesheet
#         fields = '__all__'


# class RequestWFHSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RequestWFH
#         fields = '__all__'

# class RequestUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RequestUpdate
#         fields = '__all__'

# class RequestLeaveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RequestLeave
#         fields = '__all__'