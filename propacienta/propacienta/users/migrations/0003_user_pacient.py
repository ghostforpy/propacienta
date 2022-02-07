# Generated by Django 3.2.11 on 2022-02-06 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacients', '0002_remove_pacient_user'),
        ('users', '0002_auto_20220205_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pacient',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pacients.pacient'),
        ),
    ]