# Generated by Django 3.2.11 on 2022-04-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0014_auto_20220418_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chronicdisease',
            name='treatment',
            field=models.TextField(blank=True, default='', verbose_name='Лечение'),
        ),
    ]