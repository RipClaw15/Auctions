# Generated by Django 4.2.5 on 2023-10-31 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_remove_bid_auction_bid_auction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='auction',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.CharField(default=None, max_length=16),
        ),
    ]