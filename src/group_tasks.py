""""
This file is for creating lists of tasks grouped by a keyword
"""


def group_by_task(entries: list, keywords: list[str]) -> list[list]:
    grouped = []
    for key in keywords:
        group = [entry for entry in entries if key in entry["time_entry"]["note"]]
        grouped.append(group)
    assert(len(grouped) == len(keywords))
    return grouped


def group_by_project(entries: list) -> list[list]:
    ids = []
    grouped = []
    for entry in entries:
        entry_id = entry["time_entry"]["project_id"]
        # print(entry_id)
        try:
            grouped[ids.index(entry_id)].append(entry)
        except ValueError:
            ids.append(entry_id)
            grouped.append([entry])
    # print(len(grouped))
    # print(len(ids))
    # print(ids)
    return grouped
