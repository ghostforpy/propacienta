# Generated by Django 3.2.11 on 2022-02-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_auto_20220217_2304"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
    ]
