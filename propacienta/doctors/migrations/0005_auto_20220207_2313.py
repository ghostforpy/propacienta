# Generated by Django 3.2.11 on 2022-02-07 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0004_doctor_hospitals"),
    ]

    operations = [
        migrations.CreateModel(
            name="DoctorSpecialization",
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
                        max_length=250, unique=True, verbose_name="Специализация"
                    ),
                ),
            ],
            options={
                "verbose_name": "Специализация",
                "verbose_name_plural": "Специализации",
            },
        ),
        migrations.CreateModel(
            name="DoctorSubSpecialization",
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
                        max_length=250, unique=True, verbose_name="Узкая специализация"
                    ),
                ),
                (
                    "specialization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_specializations",
                        to="doctors.doctorspecialization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Узкая специализация",
                "verbose_name_plural": "Узкие специализации",
            },
        ),
        migrations.AddField(
            model_name="doctor",
            name="specializations",
            field=models.ManyToManyField(
                related_name="doctors", to="doctors.DoctorSpecialization"
            ),
        ),
        migrations.AddField(
            model_name="doctor",
            name="sub_specializations",
            field=models.ManyToManyField(
                related_name="doctors", to="doctors.DoctorSubSpecialization"
            ),
        ),
    ]
