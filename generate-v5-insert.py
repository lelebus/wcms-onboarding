import os
import sys
import urllib3

import pandas as pd
import odswriter as ods

from utils import VColumns, fill_empty
from urllib3.exceptions import InsecureRequestWarning


V4_MATCHES_FILENAME = "v4-matches.ods"


def main(root):
    print("Root:", root)
    print("File:", V4_MATCHES_FILENAME)

    df_auto = pd.read_excel(
        os.path.join(root, V4_MATCHES_FILENAME), sheet_name="Auto (DO NOT TOUCH)"
    )
    df_manual_all = pd.read_excel(
        os.path.join(root, V4_MATCHES_FILENAME), sheet_name="Manual (insert ids)"
    )
    df_manual_mask = df_manual_all["ok"].apply(lambda x: x in (1, True, "1", "True"))
    df_manual = df_manual_all.loc[df_manual_mask].copy()
    df_forward = df_manual_all.loc[~df_manual_mask].copy()

    ############## Insert ############

    print("\nInsertion:")
    print(f"\nTotal wines: {len(df_auto) + len(df_manual) + len(df_forward)}")

    print(f"\nAutomatically matched: {len(df_auto)}")
    print(f"Manually matched: {len(df_manual)}")
    print(f"Total inserted: {len(df_auto) + len(df_manual)}")

    df_insert = pd.concat([df_auto, df_manual])

    fill_empty(df_insert, VColumns.v5()).to_csv(
        os.path.join(root, "v5-insert.csv"), index=False
    )
    print(f"Saved to {os.path.join(root, 'v5-insert.csv')}")

    ############## Forward ############
    df_forward = fill_empty(df_forward, VColumns.v2())
    df_forward = df_forward[VColumns.v2()]

    print("\nForwarding:")
    print(f"\nTo forward from matching: {len(df_forward)}")

    if os.path.exists(os.path.join(root, "v2-dropped.csv")):
        df_forward_v2 = pd.read_csv(os.path.join(root, "v2-dropped.csv"))
    else:
        df_forward_v2 = fill_empty(pd.DataFrame(), VColumns.v2())
    print(f"To forward from v2-dropped.csv: {len(df_forward_v2)}")

    with ods.writer(os.path.join(root, "v5-to-forward.ods")) as odsfile:
        for sheet_name, df in zip(
            ["From list", "From matching"],
            [df_forward_v2, df_forward],
        ):
            sheet = odsfile.new_sheet(sheet_name)
            sheet.writerow(df.columns)
            for _, row in df.fillna("").iterrows():
                sheet.writerow(row)
    print(f"Saved to {os.path.join(root, 'v5-to-forward.ods')}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v3-selection.ods")
    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

    main(os.path.join("onboardings", sys.argv[1]))
