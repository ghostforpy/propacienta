# Generated by Django 3.2.11 on 2022-03-29 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_cards', '0006_alter_resultindependentresearch_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resultindependentresearch',
            options={'ordering': ['-datetime_stamp', '-id'], 'verbose_name': 'Результат самостоятельного исследования', 'verbose_name_plural': 'Результаты самостоятельных исследований'},
        ),
    ]