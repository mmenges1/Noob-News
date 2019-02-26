# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-26 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noobnews', '0018_auto_20190225_1921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='comment_rating',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_image',
            field=models.ImageField(default='NoProfile.jpg', upload_to='static/profile_images'),
        ),
    ]
