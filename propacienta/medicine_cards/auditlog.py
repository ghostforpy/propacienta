from auditlog.registry import auditlog

from .models import MedicineCard, ResultIndependentResearch

auditlog.register(ResultIndependentResearch)
auditlog.register(MedicineCard)
