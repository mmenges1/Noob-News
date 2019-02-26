# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-24 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noobnews', '0014_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_profile_image',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='static/profile_images'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]