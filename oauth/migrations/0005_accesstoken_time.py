# Generated by Django 4.1 on 2022-10-02 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_alter_accesstoken_token_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesstoken',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
