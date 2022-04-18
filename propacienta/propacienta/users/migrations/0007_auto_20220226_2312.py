# Generated by Django 3.2.11 on 2022-02-26 20:12

from django.db import migrations, models
import propacienta.users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_email"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", propacienta.users.models.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
