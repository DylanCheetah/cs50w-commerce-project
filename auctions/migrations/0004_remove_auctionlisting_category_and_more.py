# Generated by Django 4.2.4 on 2023-08-22 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_user_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='category',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='auctions.auctioncategory'),
            preserve_default=False,
        ),
    ]
