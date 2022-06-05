# Generated by Django 3.2.11 on 2022-05-30 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_schedules', '0004_auto_20220530_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='breaks',
            field=models.JSONField(default='', help_text="Перерывы рабочего времени,\n        например {'breaks':[{'start':'1200','end':'1215'},{'start':'1515','end':'1545'}]}", verbose_name='Перерывы'),
        ),
    ]
