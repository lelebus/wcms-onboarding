import os
import sys
import urllib3
import pandas as pd
import odswriter as ods

from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning

from utils import VColumns, fill_empty


V4_MATCHES_FILENAME = "v4-matches.ods"
DUPLICATES_SUBSET = ["matched_id", "size", "vintage"]


def main(root):
    print("Root:", root)
    print("File:", V4_MATCHES_FILENAME)

    df_auto = pd.read_excel(os.path.join(root, V4_MATCHES_FILENAME), sheet_name=0)
    df_manual_all = pd.read_excel(os.path.join(root, V4_MATCHES_FILENAME), sheet_name=1)

    # set ok to False, where matched_id is empty
    df_manual_mask = df_manual_all["matched_id"].apply(lambda x: type(x) == str and len(x) == 31) 

    df_manual = df_manual_all.loc[df_manual_mask].copy()
    df_forward_manual = df_manual_all.loc[~df_manual_mask].copy()

    ############## Insert ############

    df_insert = pd.concat([df_auto, df_manual])
   # Separate rows with vintage 0
    df_vintage_zero = df_insert[df_insert["vintage"] == 0]
    df_vintage_non_zero = df_insert[df_insert["vintage"] > 0]

    # Identify duplicates, excluding rows with vintage 0
    df_forward_duplicate = df_vintage_non_zero[
        df_vintage_non_zero.duplicated(subset=DUPLICATES_SUBSET, keep=False)
    ]
    df_vintage_non_zero = df_vintage_non_zero.drop_duplicates(subset=DUPLICATES_SUBSET, keep=False)

    # Add rows with vintage 0 back to the DataFrame
    df_insert = pd.concat([df_vintage_non_zero, df_vintage_zero])
    df_insert = df_insert.rename(columns={"matched_id": "wine_id"})

    print("\nInsertion:")
    print(f"\nTotal wines: {len(df_auto) + len(df_manual_all)}")

    print(f"\nAutomatically matched: {len(df_auto)}")
    print(f"Manually matched: {len(df_manual)}")
    print(f"Duplicates: {len(df_forward_duplicate)}")
    print(f"Total inserted: {len(df_insert)}")

    fill_empty(df_insert, VColumns.v5(), True).to_csv(
        os.path.join(root, "v5-insert-draft.csv"), index=False
    )
    print(f"Saved to {os.path.join(root, 'v5-insert-draft.csv')}")

    ############## Forward ############
    df_forward_manual = fill_empty(df_forward_manual, VColumns.v2())
    df_forward_manual = df_forward_manual[VColumns.v2()]

    print("\nForwarding:")
    print(f"\nTo forward from matching: {len(df_forward_manual)}")

    if os.path.exists(os.path.join(root, "v2-dropped.csv")):
        df_forward_v2 = pd.read_csv(os.path.join(root, "v2-dropped.csv"))
    else:
        df_forward_v2 = fill_empty(pd.DataFrame(), VColumns.v2())
    print(f"To forward from v2-dropped.csv: {len(df_forward_v2)}")

    df_forward_duplicate = fill_empty(
        df_forward_duplicate, VColumns.v2() + VColumns.v3()
    ).sort_values(["matched_id", "external_id"])
    print(f"To forward from duplicates: {len(df_forward_duplicate)}")

    with ods.writer(os.path.join(root, "v5-forward-draft.ods")) as odsfile:
        for sheet_name, df in zip(
            ["From List", "From Matching", "Duplicates"],
            [df_forward_v2, df_forward_manual, df_forward_duplicate],
        ):
            if len(df) == 0:
                continue
            sheet = odsfile.new_sheet(sheet_name)
            sheet.writerow(df.columns)
            for _, row in df.fillna("").iterrows():
                sheet.writerow(row)
    print(f"Saved to {os.path.join(root, 'v5-forward-draft.ods')}")


if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v3-selection.ods")
    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

    main(os.path.join("onboardings", sys.argv[1]))
