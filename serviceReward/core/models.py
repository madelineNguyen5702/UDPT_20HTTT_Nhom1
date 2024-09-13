from django.db import models
import datetime

class Voucher(models.Model):
    MaVoucher = models.CharField(max_length=50, unique=True)
    TenVoucher = models.CharField(max_length=100, default="")
    Point = models.IntegerField()
    SoLuong = models.IntegerField()
    
    def __str__(self):
        return self.MaVoucher

    class Meta:
        db_table = 'Voucher'
        
class NV_Point(models.Model):
    MaNV = models.CharField(max_length=50)
    HoTen = models.CharField(max_length=200)
    TongPoint = models.IntegerField()
    TongVoucher = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'NV_Point'

class PointLog(models.Model):
    MaNV = models.CharField(max_length=50)
    Point = models.IntegerField()
    Loai = models.CharField(max_length=50)
    NguoiGui = models.CharField(max_length=50)
    NgayCapNhat = models.DateField()
    
    class Meta:
        managed = False
        db_table = 'PointLog'

class EmployeeVoucher(models.Model):
    MaNV = models.CharField(max_length=50)
    MaVoucher = models.CharField(max_length=50)
    NgayMua = models.DateField()
    NgaySuDung = models.DateField()
    
    class Meta:
        managed = False
        db_table = 'EmployeeVoucher'
