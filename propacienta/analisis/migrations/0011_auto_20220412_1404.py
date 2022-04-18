# Generated by Django 3.2.11 on 2022-04-12 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pacients", "0007_pacient_treating_doctors"),
        ("prescriptions", "0003_auto_20220213_1758"),
        ("medicine_cards", "0008_auto_20220412_1404"),
        ("analisis", "0010_alter_analysisresult_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="analysisresult",
            name="analysis",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysi_results",
                to="analisis.analysis",
                verbose_name="Анализ",
            ),
        ),
        migrations.AlterField(
            model_name="analysisresult",
            name="medicine_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysi_results",
                to="medicine_cards.medicinecard",
                verbose_name="Медицинская карта",
            ),
        ),
        migrations.AlterField(
            model_name="analysisresult",
            name="pacient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysi_results",
                to="pacients.pacient",
                verbose_name="Пациент",
            ),
        ),
        migrations.AlterField(
            model_name="analysisresult",
            name="prescription",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysi_results",
                to="prescriptions.analisisprescription",
                verbose_name="Назначение",
            ),
        ),
    ]
