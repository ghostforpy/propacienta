# Generated by Django 3.2.11 on 2022-05-21 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0015_auto_20220430_1547'),
        ('work_schedules', '0002_auto_20220511_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notworkingperiod',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='not_working_periods', to='doctors.doctor', verbose_name='Врач'),
        ),
    ]
