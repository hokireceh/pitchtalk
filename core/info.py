import requests

from hokireceh_claimer import base
from core.headers import headers


def get_info(data, token, proxies=None):
    url = "https://api.pitchtalk.app/v1/api/users/me"

    try:
        response = requests.get(
            url=url,
            headers=headers(data=data, token=token),
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        coins = data["coins"]
        tickets = data["tickets"]
        referral_rewards = data["referralRewards"]
        streak = data["loginStreak"]

        base.log(
            f"{base.green}Coins: {base.white}{coins:,} - {base.green}Tickets: {base.white}{tickets:,} - {base.green}Referral Rewards: {base.white}{referral_rewards} - {base.green}Streak: {base.white}{streak}"
        )
        return data
    except:
        return None
