# Generated by Django 4.1 on 2022-10-06 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0009_alter_usernametotoken_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavoranime',
            name='score',
            field=models.IntegerField(default=10, verbose_name='评分'),
        ),
    ]
