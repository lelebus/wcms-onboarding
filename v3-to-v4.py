import os
import sys
import urllib3

import pandas as pd

from utils import VColumns
from urllib3.exceptions import InsecureRequestWarning

V3_SELECTION_FILENAME = "v3-selection.ods"


def get_insert_dataframe(root, sheet_name):
    print("\nSheet:", sheet_name)
    df = pd.read_excel(os.path.join(root, V3_SELECTION_FILENAME), sheet_name=sheet_name)
    df = df.rename(columns={"matched_id": "wine_id"})
    print("Total wines:", df.shape[0])

    df = df[[el in (1, True) for el in df["ok"]]]
    ok_wines = len(df)
    print("Ok wines:", ok_wines)

    return df[VColumns.v4()]


def main(root):
    print("Root:", root)
    print("File:", V3_SELECTION_FILENAME)

    df = pd.concat(
        [
            get_insert_dataframe(root, s)
            for s in ("selection", "selection+manual", "not-found")
        ],
        ignore_index=True,
    )

    df = df.drop_duplicates()
    ok_wines = len(df)
    print("\nDuplicates removed:", len(df) - ok_wines)

    df.to_csv(os.path.join(root, "v4-insert.csv"), index=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v3-selection.ods")
    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

    main(os.path.join("onboardings", sys.argv[1]))
