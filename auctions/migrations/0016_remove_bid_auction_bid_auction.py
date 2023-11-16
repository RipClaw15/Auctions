# Generated by Django 4.2.5 on 2023-10-31 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_bid_auction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='auction',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ManyToManyField(blank=True, null=True, related_name='bidAuction', to='auctions.listing'),
        ),
    ]