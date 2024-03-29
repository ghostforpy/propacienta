# Generated by Django 3.2.11 on 2022-03-23 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("analisis", "0007_auto_20220322_0016"),
    ]

    operations = [
        migrations.AlterField(
            model_name="analysisresultsfile",
            name="analysis_result",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis_files",
                to="analisis.analysisresult",
            ),
        ),
        migrations.AlterField(
            model_name="analysisresultsimage",
            name="analysis_result",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis_images",
                to="analisis.analysisresult",
            ),
        ),
    ]
