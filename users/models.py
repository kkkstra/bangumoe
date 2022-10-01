from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    intro = models.CharField(max_length=500, verbose_name='简介')