# Generated by Django 4.2.7 on 2024-08-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_watchlist_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categories',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
