# Generated by Django 3.2.11 on 2022-02-06 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_remove_doctor_user'),
        ('pacients', '0002_remove_pacient_user'),
        ('users', '0003_user_pacient'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='doctor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='doctors.doctor'),
        ),
        migrations.AlterField(
            model_name='user',
            name='pacient',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='pacients.pacient'),
        ),
    ]