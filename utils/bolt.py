import pandas as pd
import re
from io import StringIO

def process_bolt_csv_files(file_list):
    combined_df = pd.DataFrame()

    filename_pattern = re.compile(r"^courier_orders_(\d{4})_([A-Za-z]{3})_(\d{2})\.csv$")
    month_map = {month: f"{i:02d}" for i, month in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

    for filename, file_bytes in file_list:
        if not filename_pattern.match(filename):
            continue  # Skip files that don't match pattern

        try:
            df = pd.read_csv(StringIO(file_bytes.decode('utf-8')))
            df['source_file'] = filename
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            continue

    return combined_df
