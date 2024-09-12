from rest_framework import serializers
from .models import *

from rest_framework import serializers

class VoucherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class NV_PointSerializers(serializers.ModelSerializer):
    class Meta:
        model = NV_Point
        fields = '__all__'

class EmployeeVoucherSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeVoucher
        fields = '__all__'

class PointLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = PointLog
        fields = '__all__'

