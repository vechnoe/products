# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name="Product's name")),
                ('description', models.TextField(verbose_name="Item's description")),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], max_length=255, max_digits=10, blank=True, null=True, verbose_name='Price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date', null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Update date', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
