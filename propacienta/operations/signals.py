from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import TransferredOperationFile, TransferredOperationImage


@receiver(pre_delete, sender=TransferredOperationFile)
def delete_transferred_operation_file_handler(sender, instance, **kwargs):
    instance.file.delete()


@receiver(pre_delete, sender=TransferredOperationImage)
def delete_transferred_operation_image_handler(sender, instance, **kwargs):
    instance.image.delete()
