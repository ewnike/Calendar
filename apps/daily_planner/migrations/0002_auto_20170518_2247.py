# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 03:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daily_planner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('time', models.DateTimeField(verbose_name='date_created')),
            ],
        ),
        migrations.RenameModel(
            old_name='User',
            new_name='Users',
        ),
        migrations.AddField(
            model_name='appointments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_appointments', to='daily_planner.Users'),
        ),
    ]
