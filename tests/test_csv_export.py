import pandas as pd

# We will implement this in src/... soon.
from wealth_simulator.export import dataframe_to_csv_bytes


def test_dataframe_to_csv_bytes_has_expected_header_and_rows():
    df = pd.DataFrame(
        {
            "Month": [1, 2],
            "Contributions": [100.0, 200.0],
            "Interest": [1.5, 3.0],
            "Balance": [101.5, 304.5],
            "Real Balance": [100.0, 295.0],
        }
    )

    csv_bytes = dataframe_to_csv_bytes(df)
    assert isinstance(csv_bytes, (bytes, bytearray))

    csv_text = csv_bytes.decode("utf-8")
    lines = [line.strip() for line in csv_text.strip().splitlines()]

    # Header order matters for a clean export
    assert lines[0] == "Month,Contributions,Interest,Balance,Real Balance"
    assert len(lines) == 3  # header + 2 rows