# Generated by Django 3.2.11 on 2022-04-17 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0012_auto_20220411_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='dischargeepicris',
            name='transferred_disease',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discharge_epicris', to='diseases.transferreddisease', verbose_name='Перенесённое заболенивание'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dischargeepicris',
            name='chronic_disease',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='discharge_epicrisis', to='diseases.chronicdisease', verbose_name='Хроничекое заболенивание'),
        ),
    ]
