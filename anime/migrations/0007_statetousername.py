# Generated by Django 4.1 on 2022-10-06 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0006_userfavoranime'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateToUsername',
            fields=[
                ('state', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32)),
            ],
        ),
    ]