from django.db import models
import datetime

class NhanVien(models.Model):
    
    name = models.CharField(max_length=50, unique=True, default="")
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'a'
