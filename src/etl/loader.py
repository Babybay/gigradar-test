import requests
import json
from pprint import pprint

API_URL = "http://localhost:3002/freelancers"


def load_freelancers():
    res = requests.get(API_URL, params={"page": 1, "limit": 1})
    res.raise_for_status()

    payload = res.json()

    if "items" not in payload:
        raise RuntimeError("Response does not contain 'items'")

    return payload["items"]


def inspect():
    freelancers = load_freelancers()

    print("\n=== BASIC INFO ===")
    print("Type:", type(freelancers))
    print("Count:", len(freelancers))

    first = freelancers[0]

    print("\n=== TOP-LEVEL KEYS ===")
    pprint(list(first.keys()))

    print("\n=== SAMPLE VALUES (IMPORTANT FIELDS) ===")
    sample_fields = [
        "shortName",
        "title",
        "ciphertext",
        "location",
        "hourlyRate",
        "combinedTotalEarnings",
        "totalJobs",
        "avgFeedbackScore",
        "agencies",
        "attrSkills",
        "serviceProfiles",
    ]

    for field in sample_fields:
        print(f"\n--- {field} ---")
        pprint(first.get(field))

    print("\n=== DONE ===")


if __name__ == "__main__":
    inspect()
