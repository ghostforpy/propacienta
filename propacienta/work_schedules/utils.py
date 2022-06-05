import json
from datetime import time


def decode_breaks(dct):
    if "start" in dct and "end" in dct:
        start = time(hour=int(dct["start"][:2]), minute=int(dct["start"][2:]))
        end = time(hour=int(dct["end"][:2]), minute=int(dct["end"][2:]))
        return (start, end)
    return dct


def json_to_times(s):
    if isinstance(s, dict):
        s = json.dumps(s)
    return json.loads(s, object_hook=decode_breaks)
