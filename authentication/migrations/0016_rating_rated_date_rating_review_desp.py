# Generated by Django 5.0.2 on 2024-03-10 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_remove_rating_rated_date_remove_rating_review_desp'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='rated_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='rating',
            name='review_desp',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
