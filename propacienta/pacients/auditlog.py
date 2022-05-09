from auditlog.registry import auditlog

from .models import Pacient

auditlog.register(Pacient)
