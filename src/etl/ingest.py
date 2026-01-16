import requests

BASE_URL = "http://localhost:3002/freelancers"

def fetch_all():
    page = 1
    limit = 50
    all_items = []

    while True:
        res = requests.get(BASE_URL, params={"page": page, "limit": limit})
        res.raise_for_status()
        payload = res.json()

        items = payload.get("items", [])
        if not items:
            break

        all_items.extend(items)

        if not payload.get("hasNextPage"):
            break

        page += 1

    return all_items
