from django.db import models


# Create your models here.

class ClientInformation(models.Model):
    app_name = models.CharField(primary_key=True, max_length=32, default="oidc")
    client_id = models.CharField(max_length=128)
    client_secret = models.CharField(max_length=256)
