# Generated by Django 3.2.11 on 2022-03-07 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0013_alter_doctor_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="phone",
            field=models.CharField(max_length=30, unique=True, verbose_name="Телефон"),
        ),
    ]
