# Generated by Django 4.2.7 on 2024-08-09 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('image', models.URLField(max_length=400)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listinguser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
