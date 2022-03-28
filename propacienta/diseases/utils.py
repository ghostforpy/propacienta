def discharge_epicrisis_dir(instance, filename: str) -> str:
    return "private/discharge_epicrisis/pacient_%s/%s" % (instance.discharge_epicris.pacient.id, filename)