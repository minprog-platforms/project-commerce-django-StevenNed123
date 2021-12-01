# Generated by Django 3.2.9 on 2021-11-30 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highest_bidder',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='winning_auctions', to='auctions.user'),
            preserve_default=False,
        ),
    ]