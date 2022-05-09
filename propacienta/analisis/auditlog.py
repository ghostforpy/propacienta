from auditlog.registry import auditlog

from .models import AnalysisResult, AnalysisResultsFile, AnalysisResultsImage

auditlog.register(AnalysisResultsFile)
auditlog.register(AnalysisResult)
auditlog.register(AnalysisResultsImage)
