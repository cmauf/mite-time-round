"""
This module implements the time rounding
it gets a list of time entries and a value to which it needs to round
"""


def round_single_time(time_before: int, min_entity: int):
    offset = time_before % min_entity
    if offset > min_entity/2:
        time_changed = min_entity - offset
        time_after = time_before + time_changed
    else:
        time_changed = -offset
        time_after = time_before + time_changed
    print(time_after, time_changed)
    return time_changed, time_after


def round_times(entries: list, min_entity: int):
    time_buffer = 0
    for entry in entries:
        el = entry["time_entry"]
        time_buffer, el["minutes"] = round_single_time(el["minutes"], min_entity)
