# Generated by Django 3.2.11 on 2022-02-07 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Медикамент',
                'verbose_name_plural': 'Медикаменты',
            },
        ),
    ]
