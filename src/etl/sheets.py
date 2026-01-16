import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from gspread.utils import rowcol_to_a1


SPREADSHEET_ID = "1075A7ltqIZzb-1ahCONFPB43LoQnU2bGANq4d4-F9VU"
SHEET_NAME = "Data"


def push_to_sheet(df):
    """
    Push dataframe to Google Sheets:
    - ONLY writes columns that already exist in the sheet
    - DOES NOT create new columns
    - DOES NOT overwrite existing data
    - Auto-extends rows if needed
    """

    # --- sanitize dataframe (Google Sheets strict JSON) ---
    df = df.replace([np.inf, -np.inf], None)
    df = df.astype(object)
    df = df.where(df.notna(), None)

    # --- auth ---
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    # --- read headers from sheet ---
    headers = sheet.row_values(1)
    header_index = {h.strip(): i + 1 for i, h in enumerate(headers)}

    # --- determine safe start row (use stable first column) ---
    base_col = 1  # biasanya "Do Not Delete" / ID
    start_row = len(sheet.col_values(base_col)) + 1

    # --- ensure sheet has enough rows ---
    required_rows = start_row + len(df)
    if required_rows > sheet.row_count:
        sheet.add_rows(required_rows - sheet.row_count)

    # --- write column by column ---
    for col in df.columns:
        if col not in header_index:
            # STRICT MODE: do not create / guess columns
            print(f"[SKIP] Column not found in sheet: {col}")
            continue

        col_idx = header_index[col]
        values = [[v] for v in df[col].tolist()]

        cell_range = (
            f"{rowcol_to_a1(start_row, col_idx)}:"
            f"{rowcol_to_a1(start_row + len(values) - 1, col_idx)}"
        )

        print(f"[WRITE] {col} → {cell_range}")
        sheet.update(cell_range, values)

    print("[DONE] Data pushed to Google Sheets")
