# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20151103_0625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='likers',
        ),
    ]
