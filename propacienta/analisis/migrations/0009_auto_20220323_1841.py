# Generated by Django 3.2.11 on 2022-03-23 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0008_auto_20220323_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysisresult',
            options={'ordering': ['-id'], 'verbose_name': 'Результат анализа', 'verbose_name_plural': 'Результаты анализов'},
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='result',
            field=models.TextField(null=True, verbose_name='Результаты анализа'),
        ),
    ]
