from django.db import models


# Create your models here.

class AnimeData(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    title = models.CharField(max_length=128, verbose_name="番剧名")
    episode = models.IntegerField(verbose_name="话数")
    director = models.CharField(max_length=128, verbose_name="导演")


class UserFavorAnime(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    aid = models.IntegerField(verbose_name="aid")
    title = models.CharField(max_length=128, verbose_name="番剧名")
    episode = models.IntegerField(verbose_name="话数")
    director = models.CharField(max_length=128, verbose_name="导演")
    type = models.IntegerField(default=1, verbose_name="类型")
    score = models.IntegerField(default=10, verbose_name="评分")
    comment = models.CharField(max_length=1024, verbose_name="吐槽")

class StateToUsername(models.Model):
    state = models.CharField(primary_key=True, max_length=32)
    username = models.CharField(max_length=32)

class UsernameToToken(models.Model):
    username = models.CharField(max_length=32)
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    uid = models.IntegerField()
