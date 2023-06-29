import dotenv
import json
import requests
import os
from src.time_rounding import round_times
from src.group_tasks import group_by_task
from src.tests import grouped_correct, correct_times

k = dotenv.load_dotenv(verbose=True)
config = dotenv.dotenv_values()
print(k)
print(config)
print(config['API_KEY'])

payload = {
    "api_key": f"{config['API_KEY']}",
    "from": "2023-04-01",
    "to": "today",
    "user_id": "current",
}

base_url = f"https://{config['API_DOMAIN']}.mite.de/"

# res = requests.get(
#     f"https://{config['API_DOMAIN']}.mite.de/time_entries.json",
#     params=payload
# )
# #
# k = res.json()
# print(type(k))
# print(k)
# # round_times(k, 15)
# group_tasks = group_by_task(k, ["BR", "UG"])
# grouped_correct(group_tasks, ["BR", "UG"])
#
# for group in group_tasks:
#     round_times(group, 15)
#
# new_tasks = [el for group in group_tasks for el in group]
# print(new_tasks)
with open("changed_groups.json", "r") as file:
    headers = {
        "Content-Type": "application/json",
        "X-MiteApiKey": config["API_KEY"]
    }
    k = json.load(file)
    for entry in k:
        entry_id = entry["time_entry"]["id"]
        url = base_url + f"time_entries/{entry_id}.json"
        correct_times(entry["time_entry"]["minutes"], 15)
        print(entry)
        el = {"time_entry": {"minutes": entry["time_entry"]["minutes"]}}
        print(el)
        if el["time_entry"]["minutes"] != 0:
            res = requests.patch(url,
                                 data=json.dumps(el),
                                 headers=headers)
        # else:
        #     res = requests.delete(url, headers=headers)
        print(res.url)
        print(res.status_code)
        print(res.text)
