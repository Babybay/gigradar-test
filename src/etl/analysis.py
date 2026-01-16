import pandas as pd
import numpy as np


TARGET = "Total Earnings"

CANDIDATES = [
    "Hourly Rate",
    "Total Jobs",
    "Total Hours",
    "avgFeedbackScore",
    "avgDeadlinesScore",
]


def top_3_drivers(df: pd.DataFrame):
    """
    Find top 3 variables most correlated with earnings
    """
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


def top_5_freelancers(df: pd.DataFrame):
    """
    Top 5 freelancers by total earnings
    """
    cols = [
        "Freelancer Name",
        "Company",
        "Service",
        "Skill-1",
        "Skill-2",
        "Total Earnings",
    ]

    existing = [c for c in cols if c in df.columns]

    top = (
        df[existing]
        .dropna(subset=["Total Earnings"])
        .sort_values("Total Earnings", ascending=False)
        .head(5)
    )

    return top
