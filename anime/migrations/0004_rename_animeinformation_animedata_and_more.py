# Generated by Django 4.1 on 2022-10-05 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0003_rename_animedata_animeinformation_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnimeInformation',
            new_name='AnimeData',
        ),
        migrations.RenameModel(
            old_name='UserFavorAnimeList',
            new_name='UserFavorAnime',
        ),
    ]
