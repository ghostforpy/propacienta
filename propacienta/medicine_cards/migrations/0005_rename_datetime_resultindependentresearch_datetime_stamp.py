# Generated by Django 3.2.11 on 2022-03-15 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_cards', '0004_resultindependentresearch_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultindependentresearch',
            old_name='datetime',
            new_name='datetime_stamp',
        ),
    ]