# Generated by Django 3.2.11 on 2022-03-29 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0009_auto_20220323_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysisresult',
            options={'ordering': ['-d', '-id'], 'verbose_name': 'Результат анализа', 'verbose_name_plural': 'Результаты анализов'},
        ),
    ]