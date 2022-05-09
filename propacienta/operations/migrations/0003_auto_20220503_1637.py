# Generated by Django 3.2.11 on 2022-05-03 13:37

from django.db import migrations, models
import django.db.models.deletion
import operations.utils


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_alter_operation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferredoperation',
            name='place',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='Место проведения операции'),
        ),
        migrations.AlterField(
            model_name='transferredoperation',
            name='effect',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='Эффект'),
        ),
        migrations.CreateModel(
            name='TransferredOperationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=operations.utils.transferred_operation_images_dir, verbose_name='Фото')),
                ('transferred_operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferred_operation_images', to='operations.transferredoperation')),
            ],
            options={
                'verbose_name': 'Изображение выписного эпикриза перенесенной операции',
                'verbose_name_plural': 'Изображения выписных эпикризов перенесенных операций',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TransferredOperationFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=operations.utils.transferred_operation_files_dir, verbose_name='Файл')),
                ('transferred_operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferred_operation_files', to='operations.transferredoperation')),
            ],
            options={
                'verbose_name': 'Файл выписного эпикриза перенесенной операции',
                'verbose_name_plural': 'Файлы выписных эпикризов перенесенных операций',
                'ordering': ['-id'],
            },
        ),
    ]