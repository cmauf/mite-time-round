""""
This file is for creating lists of tasks grouped by a keyword
"""

def group_by_task(entries: list, keywords: list[str]) -> list[list]:
    grouped = []
    for key in keywords:
        group = []
        for (i, entry) in enumerate(entries):
            print(i)
            if key in entry["time_entry"]["note"]:
                group.append(entry)
                entries.pop(i)
        grouped.append(group)
    assert(len(grouped) == len(keywords))
    return grouped
