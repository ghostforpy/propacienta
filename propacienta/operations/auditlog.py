from auditlog.registry import auditlog

from .models import (
    TransferredOperation,
    TransferredOperationFile,
    TransferredOperationImage,
)

auditlog.register(TransferredOperationFile)
auditlog.register(TransferredOperationImage)
auditlog.register(TransferredOperation)
