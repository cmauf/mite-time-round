import json
import click
import re
import requests
from src.time_rounding import round_times
from src.group_tasks import group_by_task, group_by_project
from src.tests import correct_times


def validate_date_string(date_string: str):
    assert(re.search("^\d{4}-\d{2}-\d{2}$", date_string) is not None)
    date = date_string.split("-")
    if int(date[0]) < 1970:
        raise click.BadParameter("There are no entries before the beginning of time!")
    elif int(date[1]) > 12 or int(date[1]) < 1:
        raise click.BadParameter("Invalid month")
    elif int(date[2]) > 31 or int(date[2]) < 0:
        raise click.BadParameter("Invalid day")
    else:
        return


def validate_time_filter(_, __, value):
    if value is None:
        return
    keywords = ["today", "yesterday", "this_week", "last_week", "this_month",
                "last_month", "this_year", "last_year"]
    k = re.search("\d{4}-\d{2}-\d{2}", value)
    if k is None and value not in keywords:
        raise click.BadParameter("Possible values: '" + "', '".join(keywords) + "'")
    elif k is not None:
        validate_date_string(value)
    return value


def fire_requests(base_url: str, api_key: str, entries: list[dict]):
    headers = {
            "Content-Type": "application/json",
            "X-MiteApiKey": api_key
    }
    for entry in entries:
        entry_id = entry["time_entry"]["id"]
        url = base_url + f"time_entries/{entry_id}.json"
        correct_times(entry["time_entry"]["minutes"], 15)
        # print(entry)
        el = {"time_entry": {"minutes": entry["time_entry"]["minutes"]}}
        # print(el)
        if el["time_entry"]["minutes"] != 0:
            requests.patch(url,
                           data=json.dumps(el),
                           headers=headers)
        else:
            requests.delete(url, headers=headers)


def project_round_times(project: list[dict], tags: list[str], min_: int) -> list[dict]:
    new_tasks = []
    if len(tags) > 0:
        tasks = group_by_task(project, tags)
        for task in tasks:
            round_times(task, min_)
            new_tasks += task
    else:
        new_tasks = round_times(project, min_)
    assert(len(new_tasks) == len(project))
    return new_tasks


@click.command()
@click.option("-d", "--domain", "domain", type=str,
              help="The mite subdomain your company occupies",
              prompt="Your mite subdomain")
@click.option("-key", "--api-key", "api_key", type=str,
              help="Your key for the mite API", prompt="Your API key")
@click.option("-res", "--ressource", "ressource", type=str,
              help="Which ressource to access", default="time_entries")
@click.option("-min", "--min-round-entity", "min_", type=int, default=15,
              help="Smallest time entity to round to (in minutes)")
@click.option("-t", "--tags", "tags", multiple=True,
              help="Identifying tags for different tasks in the same project")
@click.option("--group-projects/--no-group-projects", default=True,
              help="Group by project or all together")
@click.option("-at", default="this_month", help="The time frame to show.",
              type=click.UNPROCESSED,
              callback=validate_time_filter)
@click.option("-to", "to", help="The start for filtering entries",
              type=click.UNPROCESSED,
              callback=validate_time_filter)
@click.option("-f", "--from", "from_", help="The end for filtering entries",
              type=click.UNPROCESSED,
              callback=validate_time_filter)
@click.option("-i", "--interactive", is_flag=True, help="Use interactive CLI dialog")
def main(domain, api_key, ressource, min_, tags,
         group_projects, at, to, from_, interactive):
    if (to is None and from_ is not None) or (to is not None and from_ is None):
        raise click.BadArgumentUsage(
            "Both 'to' and 'from' parameters have to be provided"
        )
    if interactive:
        pass  # implement interactive CLI dialog
    base_url = f"https://{domain}.mite.de/"
    payload = {
        "api_key": f"{api_key}",
        "user_id": "current",
    }
    if to is not None:  # exception guarantees that `_from` is not None either
        payload["to"] = to
        payload["from"] = from_
    else:
        payload["at"] = at

    res = requests.get(
        f"{base_url}/{ressource}.json",
        params=payload
    ).json()
    print(len(res))
    changed_entries = []
    if group_projects:
        projects = group_by_project(res)
        for project in projects:
            new_times = project_round_times(project, tags, min_)
            changed_entries += new_times
    else:
        changed_entries = project_round_times(res, tags, min_)

    print(len(changed_entries))
    assert(len(changed_entries) == len(res))
    fire_requests(base_url, api_key, changed_entries)


if __name__ == "__main__":
    main()
