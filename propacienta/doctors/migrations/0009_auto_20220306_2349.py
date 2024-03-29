# Generated by Django 3.2.11 on 2022-03-06 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospitals", "0003_alter_hospitaltown_options"),
        ("doctors", "0008_doctor_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="hospitals",
            field=models.ManyToManyField(
                null=True,
                related_name="doctors",
                to="hospitals.Hospital",
                verbose_name="Клиники",
            ),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="specializations",
            field=models.ManyToManyField(
                null=True,
                related_name="doctors",
                to="doctors.DoctorSpecialization",
                verbose_name="Специализации",
            ),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="sub_specializations",
            field=models.ManyToManyField(
                null=True,
                related_name="doctors",
                to="doctors.DoctorSubSpecialization",
                verbose_name="Узкие специализации",
            ),
        ),
    ]
