from django.db import models

# Create your models here.

MEDIA_ADDRESS = "http://localhost:8000/media/"

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="uid")
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    intro = models.CharField(max_length=512, default="这个人很懒，什么都没有留下。", verbose_name="简介")

    def __str__(self):
        return self.id
