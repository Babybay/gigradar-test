from ingest import fetch_all
from transform import transform
from sheets import push_to_sheet
from analysis import run_analysis

if __name__ == "__main__":
    raw = fetch_all()
    df = transform(raw)

    if df.empty:
        raise RuntimeError("No data to upload")

    push_to_sheet(df)
    print("DONE")

    run_analysis(df)

