# Generated by Django 4.1 on 2022-10-02 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('app_name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('client_id', models.CharField(max_length=128)),
                ('client_secret', models.CharField(max_length=256)),
                ('client_type', models.IntegerField(default=1)),
                ('redirect_url', models.URLField(max_length=512)),
            ],
        ),
    ]