# Generated by Django 4.2.4 on 2023-08-23 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]