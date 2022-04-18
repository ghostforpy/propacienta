# Generated by Django 3.2.11 on 2022-02-07 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HospitalTown",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Наименование"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hospital",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Наименование"
                    ),
                ),
                ("address", models.CharField(max_length=250, verbose_name="Адрес")),
                (
                    "town",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="hospitals",
                        to="hospitals.hospitaltown",
                        verbose_name="Населенный пункт",
                    ),
                ),
            ],
        ),
    ]
