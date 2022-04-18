# Generated by Django 3.2.11 on 2022-02-13 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pacients", "0003_alter_pacient_options"),
        ("medicine_cards", "0003_auto_20220212_1109"),
        ("diseases", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransferredDisease",
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
                ("diagnosis", models.CharField(max_length=250, verbose_name="Диагноз")),
                (
                    "diagnosis_date",
                    models.DateField(
                        null=True, verbose_name="Дата постановки диагноза"
                    ),
                ),
                (
                    "diagnosis_year",
                    models.PositiveIntegerField(
                        null=True, verbose_name="Год постановки диагноза"
                    ),
                ),
                (
                    "treatment_date",
                    models.DateField(null=True, verbose_name="Дата начала лечения"),
                ),
                (
                    "treatment_end_date",
                    models.DateField(null=True, verbose_name="Дата окончания лечения"),
                ),
                (
                    "disease",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="transferred_diseases",
                        to="diseases.disease",
                        verbose_name="Заболенивание",
                    ),
                ),
                (
                    "medicine_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="transferred_diseases",
                        to="medicine_cards.medicinecard",
                        verbose_name="Медицинская карта",
                    ),
                ),
                (
                    "pacient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="transferred_diseases",
                        to="pacients.pacient",
                        verbose_name="Пациент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Перенесенное заболевание",
                "verbose_name_plural": "Перенесенные заболевания",
            },
        ),
    ]
