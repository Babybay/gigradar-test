import pandas as pd
from sheets import push_analysis_sheet


TARGET = "Total Earnings"
CANDIDATES = [
    "Hourly Rate",
    "Total Jobs",
    "Total Hours",
    "avgFeedbackScore",
    "avgDeadlinesScore",
]

def only_ready(df):
    if "Status" not in df.columns:
        raise ValueError("Status column not found in DataFrame")
    return df[df["Status"] == "READY"].copy()


def top_3_drivers(df):
    results = []

    for col in CANDIDATES:
        if col not in df.columns:
            continue

        sub = df[[TARGET, col]].dropna()
        if len(sub) < 10:
            continue

        corr = sub[TARGET].corr(sub[col])
        if pd.notna(corr):
            results.append((col, abs(corr)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:3]


def top_5_freelancers(df):
    cols = [
        "TEMP09-shortName",
        "TEMP12-companyFullName",
        "Job Title",
        "TEMP06-skill1",
        "TEMP07-skill2",
        "PD02-combinedTotalRevenue",
    ]

    return (
        df[cols]
        .dropna(subset=["PD02-combinedTotalRevenue"])
        .sort_values("PD02-combinedTotalRevenue", ascending=False)
        .head(5)
    )



def run_analysis(df):
    df_ready = only_ready(df)

    if df_ready.empty:
        print("[ANALYSIS] No READY data found. Skipping analysis.")
        return

    drivers_df = top_3_drivers(df_ready)
    top5_df = top_5_freelancers(df_ready)

    push_analysis_sheet(drivers_df, top5_df)

