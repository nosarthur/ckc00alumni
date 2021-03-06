# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-09 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_myuser_referred_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.RenameField(
            model_name='myuser',
            old_name='company',
            new_name='employer',
        ),
        migrations.AddField(
            model_name='myuser',
            name='homepage',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='api.Tag'),
        ),
    ]
