# Generated by Django 3.2.14 on 2023-06-21 18:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrequest',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 21, 18, 4, 23, 756348, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
