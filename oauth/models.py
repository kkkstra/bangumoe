from django.db import models


# Create your models here.

class Application(models.Model):
    app_name = models.CharField(primary_key=True, max_length=32)
    client_id = models.CharField(max_length=128)
    client_secret = models.CharField(max_length=256)
    client_type = models.IntegerField(default=1)  # 0为public，1为confidential
    redirect_url = models.URLField(max_length=512)

    def __str__(self):
        return self.app_name


class AuthorizationCode(models.Model):
    client_id = models.CharField(primary_key=True, max_length=128)
    code = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now=True)  # 创建时间
    scope = models.CharField(max_length=128, default="default")

    def __str__(self):
        return self.client_id


class AccessToken(models.Model):
    time = models.DateTimeField(auto_now=True)  # 创建时间
    access_token = models.CharField(max_length=256)
    token_type = models.CharField(max_length=256, default="bearer")
    expires_in = models.IntegerField(default=60)
    refresh_token = models.CharField(max_length=256)
    scope = models.CharField(max_length=128, default="default")

    def __str__(self):
        return self.access_token
