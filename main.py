import dotenv
import json
import requests

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
    "group_by": "project"
}

# res = requests.get(
#     f"https://{config['API_DOMAIN']}.mite.de/time_entries.json",
#     params=payload
# )
# print(type(res.json()))
# with open("res_grouped.json", "w") as grouped_file:
#     grouped_file.write(res.text)
with open("src/res.json", "r") as file:
    k = json.load(file)
    print(type(k))
