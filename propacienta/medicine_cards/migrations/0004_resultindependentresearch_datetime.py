# Generated by Django 3.2.11 on 2022-03-15 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medicine_cards", "0003_auto_20220212_1109"),
    ]

    operations = [
        migrations.AddField(
            model_name="resultindependentresearch",
            name="datetime",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Время проведения"
            ),
        ),
    ]
