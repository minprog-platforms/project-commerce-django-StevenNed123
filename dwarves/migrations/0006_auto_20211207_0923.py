# Generated by Django 3.2.9 on 2021-12-07 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwarves', '0005_alter_dwarf_portrait'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mineral',
            old_name='Mine',
            new_name='mine',
        ),
        migrations.RenameField(
            model_name='mineral',
            old_name='Name',
            new_name='name',
        ),
    ]
