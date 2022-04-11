# Generated by Django 3.2.11 on 2022-03-29 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0004_auto_20220329_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferreddisease',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transferred_diseases', to='diseases.disease', verbose_name='Заболевание'),
        ),
    ]
