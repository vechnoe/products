# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name="Comment's body")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date', null=True)),
                ('product', models.ForeignKey(verbose_name='Commentary', to='products.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
