# Generated by Django 5.0.2 on 2024-03-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_restaurant_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='review_desp',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
