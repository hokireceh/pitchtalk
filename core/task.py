import requests

from hokireceh_claimer import base
from core.headers import headers


def get_task(token, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/tasks"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()

        return data
    except:
        return None


def do_task(token, task_id, proxies=None):
    url = f"https://api.pitchtalk.app/v1/api/tasks/{task_id}/start"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["status"]

        return status
    except:
        return None


def verify(token, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/tasks/verify"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()

        return data
    except:
        return None


def process_do_task(token, proxies=None):
    task_list = get_task(token=token, proxies=proxies)
    for task in task_list:
        task_id = task["id"]
        task_status = task["status"]
        task_name = task["template"]["title"]

        if task_status == "COMPLETED_CLAIMED":
            base.log(f"{base.white}{task_name}: {base.green}Completed")
        else:
            do_task_status = do_task(token=token, task_id=task_id, proxies=proxies)
            verify_list = verify(token=token, proxies=proxies)
            verify_status = next(
                (item["status"] for item in verify_list if item["id"] == task_id),
                "Not found",
            )
            if verify_status == "COMPLETED_CLAIMED":
                base.log(
                    f"{base.white}{task_name}: {base.yellow}{do_task_status} -> {base.green}{verify_status}"
                )
            else:
                base.log(
                    f"{base.white}{task_name}: {base.yellow}{do_task_status} -> {base.red}{verify_status}"
                )
