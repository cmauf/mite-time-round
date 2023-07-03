"""
This file contains tests for several things
"""


def grouped_correct(list_tasks, keywords):
    for (i, list_entry) in enumerate(list_tasks):
        # print(keywords[i])
        for entry in list_entry:
            assert keywords[i] in entry["time_entry"]["note"]


def sum_up_times(entries):
    total = 0
    for entry in entries:
        total += entry["time_entry"]["minutes"]
    return total


def correct_times(time, min_entity):
    assert(time % min_entity == 0)
