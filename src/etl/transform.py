import pandas as pd

def safe_get(d, path):
    """
    Safe getter for nested dict/list using path list
    """
    try:
        for p in path:
            d = d[p]
        return d
    except (KeyError, IndexError, TypeError):
        return None

def is_ready(row: dict) -> bool:
    required_fields = [
        "TEMP09-shortName",
        "TEMP12-companyFullName",
        "TEMP15-upworkUrl",
        "Job Title",
        "TEMP06-skill1",
        "TEMP07-skill2",
        "PD02-combinedTotalRevenue",
    ]

    for field in required_fields:
        if not row.get(field):
            return False
    return True


def transform(freelancers):
    rows = []

    for f in freelancers:
        row = {
            # === IDENTIFIER ===
            "TEMP08-ciphertext": f.get("ciphertext"),
            "TEMP09-shortName": f.get("shortName"),

            # === COMPANY ===
            "TEMP12-companyFullName": safe_get(f, ["agencies", 0, "name"]),
            "PD06-Company-Country": safe_get(f, ["location", "country"]),

            # === URL ===
            "TEMP15-upworkUrl": (
                f"https://www.upwork.com/freelancers/~{f.get('ciphertext')}"
                if f.get("ciphertext") else None
            ),

            # === PROFILE ===
            "Job Title": f.get("title"),
            "TEMP10-memberSince": f.get("memberSince"),
            "TEMP05-summarySanitized": (
                f.get("profileSummary")
                or f.get("overview")
                or f.get("description")
            ),

            # === SKILLS ===
            "TEMP06-skill1": safe_get(f, ["attrSkills", 0, "groupName"]),
            "TEMP07-skill2": safe_get(
                f, ["attrSkills", 0, "skills", 0, "skill", "name"]
            ),

            # === METRICS ===
            "PD03-totalHourlyJobs": safe_get(
                f, ["serviceProfiles", 0, "aggregates", "totalHours"]
            ),
            "PD14-combinedRecentEarnings": safe_get(
                f, ["serviceProfiles", 0, "aggregates", "totalCharge"]
            ),
            "PD02-combinedTotalRevenue": safe_get(
                f, ["serviceProfiles", 0, "aggregates", "totalCharge"]
            ),

            # === SCORES ===
            "TEMP15-avgFeedbackscore": f.get("avgFeedbackScore"),
            "TEMP02-avgDeadlinesScore": f.get("avgDeadlinesScore"),
        }
        row["Status"] = "READY" if is_ready(row) else None

        rows.append(row)


    return pd.DataFrame(rows)
