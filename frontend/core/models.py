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
