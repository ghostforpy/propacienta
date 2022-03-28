# Generated by Django 3.2.11 on 2022-03-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0003_alter_disease_code'),
        ('analisis', '0005_auto_20220320_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='diseases',
            field=models.ManyToManyField(blank=True, related_name='analyzis', to='diseases.Disease', verbose_name='Заболевания'),
        ),
    ]
