# Generated by Django 3.2.11 on 2022-02-06 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctor",
            name="user",
        ),
    ]
