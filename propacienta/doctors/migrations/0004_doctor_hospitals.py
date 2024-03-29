# Generated by Django 3.2.11 on 2022-02-07 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospitals", "0002_alter_hospital_options"),
        ("doctors", "0003_alter_doctor_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="hospitals",
            field=models.ManyToManyField(
                related_name="doctors", to="hospitals.Hospital", verbose_name="Клиники"
            ),
        ),
    ]
