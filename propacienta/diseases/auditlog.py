from auditlog.registry import auditlog

from .models import (
    ChronicDisease,
    DischargeEpicris,
    DischargeEpicrisFiles,
    DischargeEpicrisImage,
    TransferredDisease,
)

auditlog.register(ChronicDisease)
auditlog.register(DischargeEpicris)
auditlog.register(DischargeEpicrisFiles)
auditlog.register(DischargeEpicrisImage)
auditlog.register(TransferredDisease)
