# Generated by Django 3.2.9 on 2021-12-06 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dwarves', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mine',
            name='minerals',
        ),
        migrations.RemoveField(
            model_name='upgrade',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='user',
            name='inventory',
        ),
        migrations.AddField(
            model_name='mineral',
            name='Mine',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='minerals', to='dwarves.mine'),
        ),
        migrations.AddField(
            model_name='mineral',
            name='upgrade',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost', to='dwarves.upgrade'),
        ),
        migrations.AddField(
            model_name='mineral',
            name='user',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to=settings.AUTH_USER_MODEL),
        ),
    ]
