from __future__ import annotations


import pandas as pd


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """
    Convert a simulation results DataFrame to UTF-8 CSV bytes.

    Keeps the current column order as-is to ensure stable exports.
    """
    csv_text = df.to_csv(index=False, lineterminator="\n")
    return csv_text.encode("utf-8")