# Generated by Django 4.1 on 2022-10-07 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activated',
            field=models.BooleanField(default=False, verbose_name='激活状态'),
        ),
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(default=0, max_length=10, verbose_name='激活验证码'),
            preserve_default=False,
        ),
    ]
