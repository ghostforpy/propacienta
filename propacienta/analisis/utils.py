def analisis_result_dir(instance, filename: str) -> str:
    return "analisis_results/pacient_%s/%s" % (instance.analysis_result.pacient.id, filename)