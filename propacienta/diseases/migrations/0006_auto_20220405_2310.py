# Generated by Django 3.2.11 on 2022-04-05 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diseases", "0005_alter_transferreddisease_disease"),
    ]

    operations = [
        migrations.AddField(
            model_name="dischargeepicris",
            name="treatment",
            field=models.TextField(null=True, verbose_name="Эпикриз"),
        ),
        migrations.AlterField(
            model_name="chronicdisease",
            name="treatment",
            field=models.TextField(null=True, verbose_name="Лечение"),
        ),
    ]
