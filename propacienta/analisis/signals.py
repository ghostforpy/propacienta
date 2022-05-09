from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import AnalysisResultsFile, AnalysisResultsImage


@receiver(pre_delete, sender=AnalysisResultsFile)
def delete_analysis_results_file_handler(sender, instance, **kwargs):
    instance.file.delete()


@receiver(pre_delete, sender=AnalysisResultsImage)
def delete_analysis_results_image_handler(sender, instance, **kwargs):
    instance.image.delete()
