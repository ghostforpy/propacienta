# Generated by Django 3.2.11 on 2022-02-09 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("appointments", "0004_alter_appointmentsurvey_options"),
        ("procedures", "0001_initial"),
        ("medicines", "0001_initial"),
        ("analisis", "0001_initial"),
        ("medicine_cards", "0001_initial"),
        ("doctors", "0006_auto_20220207_2326"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcedurePrescription",
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
                    "duration",
                    models.PositiveIntegerField(verbose_name="Продолжительность"),
                ),
                ("rate", models.PositiveIntegerField(verbose_name="Частота")),
                ("number", models.FloatField(verbose_name="Количество")),
                (
                    "per",
                    models.CharField(
                        help_text="День, неделя, месяц, час",
                        max_length=20,
                        verbose_name="Единица измерения частоты",
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="procedureprescription",
                        to="doctors.doctor",
                    ),
                ),
                (
                    "doctor_appointment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="procedureprescription",
                        to="appointments.doctorappointment",
                    ),
                ),
                (
                    "medicine_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="procedureprescription",
                        to="medicine_cards.medicinecard",
                    ),
                ),
                (
                    "procedure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="procedure_prescriptions",
                        to="procedures.procedure",
                    ),
                ),
            ],
            options={
                "verbose_name": "Назначение процедуры",
                "verbose_name_plural": "Назначения процедур",
            },
        ),
        migrations.CreateModel(
            name="MedicinePrescription",
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
                    "duration",
                    models.PositiveIntegerField(verbose_name="Продолжительность"),
                ),
                ("rate", models.PositiveIntegerField(verbose_name="Частота")),
                ("number", models.FloatField(verbose_name="Количество")),
                (
                    "per",
                    models.CharField(
                        help_text="День, неделя, месяц, час",
                        max_length=20,
                        verbose_name="Единица измерения частоты",
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="medicineprescription",
                        to="doctors.doctor",
                    ),
                ),
                (
                    "doctor_appointment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="medicineprescription",
                        to="appointments.doctorappointment",
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="medicine_prescriptions",
                        to="medicines.medicine",
                    ),
                ),
                (
                    "medicine_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="medicineprescription",
                        to="medicine_cards.medicinecard",
                    ),
                ),
            ],
            options={
                "verbose_name": "Назначение медикаментов",
                "verbose_name_plural": "Назначения медикаментов",
            },
        ),
        migrations.CreateModel(
            name="AnalisisPrescription",
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
                    "analisis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="analisis_prescriptions",
                        to="analisis.analysis",
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="analisisprescription",
                        to="doctors.doctor",
                    ),
                ),
                (
                    "doctor_appointment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="analisisprescription",
                        to="appointments.doctorappointment",
                    ),
                ),
                (
                    "medicine_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="analisisprescription",
                        to="medicine_cards.medicinecard",
                    ),
                ),
            ],
            options={
                "verbose_name": "Назначение анализа",
                "verbose_name_plural": "Назначения анализов",
            },
        ),
    ]
