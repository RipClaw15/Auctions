# Generated by Django 4.2.5 on 2023-10-31 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_remove_bid_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
