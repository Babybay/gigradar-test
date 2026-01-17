import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from gspread.utils import rowcol_to_a1


SPREADSHEET_ID = "1075A7ltqIZzb-1ahCONFPB43LoQnU2bGANq4d4-F9VU"
DATA_SHEET = "Data"
ANALYSIS_SHEET = "Analysis"


def _get_client():
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return gspread.authorize(creds)


def push_to_sheet(df):
    df = df.replace([np.inf, -np.inf], None)
    df = df.astype(object)
    df = df.where(df.notna(), None)

    client = _get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(DATA_SHEET)

    headers = sheet.row_values(1)
    header_index = {h.strip(): i + 1 for i, h in enumerate(headers)}

    base_col = 1
    start_row = len(sheet.col_values(base_col)) + 1

    required_rows = start_row + len(df)
    if required_rows > sheet.row_count:
        sheet.add_rows(required_rows - sheet.row_count)

    for col in df.columns:
        if col not in header_index:
            continue

        col_idx = header_index[col]
        values = [[v] for v in df[col].tolist()]
        rng = (
            f"{rowcol_to_a1(start_row, col_idx)}:"
            f"{rowcol_to_a1(start_row + len(values) - 1, col_idx)}"
        )
        sheet.update(rng, values)


def get_or_create_analysis_sheet():
    client = _get_client()
    ss = client.open_by_key(SPREADSHEET_ID)

    try:
        return ss.worksheet(ANALYSIS_SHEET)
    except gspread.WorksheetNotFound:
        return ss.add_worksheet(title=ANALYSIS_SHEET, rows=100, cols=20)


def push_analysis_sheet(drivers, top5_df):
    sheet = get_or_create_analysis_sheet()
    sheet.clear()

    row = 1
    sheet.update(f"A{row}", [["Top 3 Variables Impacting Earnings"]])
    row += 1
    sheet.update(f"A{row}", [["Variable", "Correlation"]])
    row += 1

    for var, score in drivers:
        sheet.update(f"A{row}", [[var, round(score, 3)]])
        row += 1

    row += 2
    sheet.update(f"A{row}", [["Top 5 Highest-Earning Freelancers"]])
    row += 1
    sheet.update(f"A{row}", [top5_df.columns.tolist()])
    row += 1
    sheet.update(f"A{row}", top5_df.values.tolist())
