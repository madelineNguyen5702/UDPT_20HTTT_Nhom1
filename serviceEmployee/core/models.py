from django.db import models
import datetime

class NhanVien(models.Model):
    MaNV = models.CharField(max_length=50, unique=True)
    MatKhau = models.CharField(max_length=50, default="123")
    HoTen = models.CharField(max_length=200, default="")
    GioiTinh = models.CharField(max_length=10, default="")
    CCCD = models.CharField(max_length=20, unique=True, default="")
    NgaySinh = models.DateField(default=datetime.date(2000, 1, 1))
    MaSoThue = models.CharField(max_length=20, unique=True, default="")
    DiaChi = models.CharField(max_length=100, default="")
    SDT = models.CharField(max_length=20, unique=True, default="")
    Email = models.CharField(max_length=50, unique=True, default="")
    STK = models.CharField(max_length=50, unique=True, default="")
    
    def __str__(self):
        return self.MaNV

    class Meta:
        db_table = 'NhanVien'
        
class DanhSachNhanVienQuanLy(models.Model):
    MaNV = models.CharField(max_length=50)
    HoTen = models.CharField(max_length=200)
    GioiTinh = models.CharField(max_length=10)
    NgaySinh = models.DateField()
    DiaChi = models.CharField(max_length=100)
    SDT = models.CharField(max_length=20)
    Email = models.CharField(max_length=50)
    MaQL = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'NV_QL'

class Timesheet(models.Model):
    Ngay = models.DateField()
    MaNV = models.CharField(max_length=50)
    Checkin = models.TimeField()
    Checkout = models.TimeField()
    isLeave = models.BooleanField()
    isWFH = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'Timesheet'


class RequestLeave(models.Model):
    MaYC = models.CharField(max_length=50)
    MaNV = models.CharField(max_length=50)
    NgayGui = models.DateTimeField()
    NgayDuyet = models.DateTimeField()
    NgayRequest = models.DateTimeField()
    TrangThai = models.CharField(max_length=50)
    IDNguoiDuyet = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'NV_RequestLeave'

class RequestWFH(models.Model):
    MaYC = models.CharField(max_length=50)
    MaNV = models.CharField(max_length=50)
    NgayGui = models.DateTimeField()
    NgayDuyet = models.DateTimeField()
    NgayRequest = models.DateTimeField()
    TrangThai = models.CharField(max_length=50)
    IDNguoiDuyet = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'NV_RequestWFH'

class RequestUpdate(models.Model):
    MaYC = models.CharField(max_length=50)
    MaNV = models.CharField(max_length=50)
    Ngay = models.DateField()
    Checkin = models.TimeField()
    updateCheckin = models.TimeField()
    Checkout = models.TimeField()
    updateCheckout = models.TimeField()
    NgayGui = models.DateTimeField()
    ChiTiet = models.CharField(max_length=50)
    TrangThai = models.CharField(max_length=50)
    NgayDuyet = models.DateTimeField()
    IDNguoiDuyet = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'NV_RequestUpdate'
