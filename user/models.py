import os

from django.db import models


# Create your models here.

# def user_directory_path(instance, filename):
#     ext = filename.split('.').pop()
#     filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
#     return os.path.join(instance.major.name, filename)


class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="uid")
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=512, verbose_name="密码")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    intro = models.CharField(max_length=512, default="这个人很懒，什么都没有留下。", verbose_name="简介")
    activated = models.BooleanField(default=False, verbose_name="激活状态")
    code = models.CharField(max_length=10, verbose_name="激活验证码")

    # avatar = models.ImageField('头像', upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return self.id

    # 用户注册时没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径
    # def photo_url(self):
    #     if self.avatar and hasattr(self.avatar, 'url'):
    #         return self.avatar.url
    #     else:
    #         return '/media/default/user.jpg'


# 好友关系
class UserRelation(models.Model):
    uid_from = models.IntegerField()
    uid_to = models.IntegerField()


# 好友请求
class FriendsRequest(models.Model):
    uid_from = models.IntegerField()
    uid_to = models.IntegerField()
    username_from = models.CharField(max_length=32)
    username_to = models.CharField(max_length=32)
    msg = models.CharField(max_length=512)
    status = models.IntegerField(default=1) # 1为待通过，2为已通过，3为已拒绝
