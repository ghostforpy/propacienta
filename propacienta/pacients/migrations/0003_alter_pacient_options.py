# Generated by Django 3.2.11 on 2022-02-06 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacients', '0002_remove_pacient_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pacient',
            options={'verbose_name': 'Пациент', 'verbose_name_plural': 'Пациенты'},
        ),
    ]