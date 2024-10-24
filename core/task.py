import requests
import random
import string

from hokireceh_claimer import base
from core.headers import headers
from core.info import get_info


def get_task(data, token, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/tasks"

    try:
        response = requests.get(
            url=url,
            headers=headers(data=data, token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def do_task(data, token, task_id, proxies=None):
    url = f"https://api.pitchtalk.app/v1/api/tasks/{task_id}/start"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data, token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["status"]

        return status
    except:
        return None


def verify(data, token, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/tasks/verify"

    try:
        response = requests.get(
            url=url,
            headers=headers(data=data, token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def create_daily(data, token, slug, proof, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/tasks/create-daily"
    payload = {"slug": slug, "proof": proof}

    try:
        response = requests.post(
            url=url,
            headers=headers(data, token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def generate_random_links():
    # Generate random username (between 5 and 20 characters)
    username_length = random.randint(5, 20)
    username = "".join(
        random.choices(string.ascii_letters + string.digits, k=username_length)
    )

    # Generate random IDs for X and TikTok links
    x_status_id = random.randint(10**17, 10**18)
    tiktok_photo_id = random.randint(10**15, 10**18)

    # Construct the X and TikTok links
    x_link = f"https://x.com/{username}/status/{x_status_id}"
    tiktok_link = f"https://www.tiktok.com/@{username}/photo/{tiktok_photo_id}"

    return x_link, tiktok_link


def process_do_task(data, token, proxies=None):
    task_list = get_task(data=data, token=token, proxies=proxies)
    for task in task_list:
        task_id = task["id"]
        task_status = task["status"]
        task_name = task["template"]["title"]

        if task_status == "COMPLETED_CLAIMED":
            base.log(f"{base.white}{task_name}: {base.green}Completed")
        else:
            do_task_status = do_task(
                data=data, token=token, task_id=task_id, proxies=proxies
            )
            verify_list = verify(data=data, token=token, proxies=proxies)
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

    x_link, tiktok_link = generate_random_links()

    daily_tasks = [
        {
            "slug": "share-x",
            "proof": x_link,
        },
        {
            "slug": "share-tiktok",
            "proof": tiktok_link,
        },
    ]

    for daily_task in daily_tasks:
        slug = daily_task["slug"]
        proof = daily_task["proof"]
        do_daily_task = create_daily(
            data=data, token=token, slug=slug, proof=proof, proxies=proxies
        )
        try:
            daily_task_name = do_daily_task["template"]["title"]
            daily_task_status = do_daily_task["status"]
            base.log(f"{base.white}{daily_task_name}: {base.yellow}{daily_task_status}")
        except:
            msg = do_daily_task["message"].split(":")[1].strip()
            base.log(f"{base.white}Daily tasks: {base.red}{msg}")


def claim_referral(data, token, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/users/claim-referral"

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data, token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def process_claim_ref(data, token, proxies=None):
    referral_rewards = get_info(data=data, token=token, proxies=proxies)[
        "referralRewards"
    ]
    if referral_rewards > 0:
        start_claim_ref = claim_referral(data=data, token=token, proxies=proxies)
        get_info(data=data, token=token, proxies=proxies)
    else:
        base.log(f"{base.white}Auto Claim Ref: {base.red}No point from ref")
