from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import DischargeEpicrisFiles, DischargeEpicrisImage


@receiver(pre_delete, sender=DischargeEpicrisFiles)
def delete_discharge_epicris_file_handler(sender, instance, **kwargs):
    instance.file.delete()


@receiver(pre_delete, sender=DischargeEpicrisImage)
def delete_discharge_epicris_image_handler(sender, instance, **kwargs):
    instance.image.delete()
