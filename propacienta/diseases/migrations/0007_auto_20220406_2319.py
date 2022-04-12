# Generated by Django 3.2.11 on 2022-04-06 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0006_auto_20220405_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chronicdisease',
            name='treatment',
            field=models.TextField(blank=True, null=True, verbose_name='Лечение'),
        ),
        migrations.AlterField(
            model_name='dischargeepicris',
            name='treatment',
            field=models.TextField(blank=True, null=True, verbose_name='Эпикриз'),
        ),
    ]