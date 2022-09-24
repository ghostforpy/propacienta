# Generated by Django 3.2.11 on 2022-09-20 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webdials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webdial',
            name='end_webdial',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Окончание разговора'),
        ),
        migrations.AlterField(
            model_name='webdial',
            name='webdial_duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Продолжительность разговора'),
        ),
    ]