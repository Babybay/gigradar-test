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
    drivers = top_3_drivers(df)
    top5 = top_5_freelancers(df)
    push_analysis_sheet(drivers, top5)
