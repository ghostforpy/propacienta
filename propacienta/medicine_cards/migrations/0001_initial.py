# Generated by Django 3.2.11 on 2022-02-06 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pacients", "0003_alter_pacient_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicineCard",
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
                    "height",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, null=True, verbose_name="Height"
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, null=True, verbose_name="Weight"
                    ),
                ),
                ("average_pressure", models.CharField(max_length=20, null=True)),
                (
                    "pacient",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medicine_card",
                        to="pacients.pacient",
                        verbose_name="Medicine card",
                    ),
                ),
            ],
            options={
                "verbose_name": "Медицинская карта",
                "verbose_name_plural": "Медицинские карты",
            },
        ),
    ]
