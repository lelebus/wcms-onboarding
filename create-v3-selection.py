import os
import sys
import json
import pandas as pd

import odswriter as ods


class V3SpreadsheetWriter:
    OUTPUT_FILENAME = "v3-selection-draft.ods"

    def __init__(self, root):
        self.root = root

        self._read_sheets()
        self._save()

    def _write_selection_manual(self, cols):
        df = pd.DataFrame(columns=self.df_m.columns)
        df["ok"] = False
        df = df[cols]

        return df

    @classmethod
    def get_cols(cls):
        with open("utils/v2-columns.json") as f:
            cols = json.load(f)
        with open("utils/v3-columns.json") as f:
            cols += json.load(f)
        return ["ok"] + cols

    def _read_sheets(self):
        df_m = pd.read_csv(os.path.join(self.root, "v3-matches.csv"))
        df_m["ok"] = False

        df_nf = pd.read_csv(os.path.join(self.root, "v3-not-found.csv"))
        df_nf["ok"] = [
            ods.Formula(f"NOT(ISBLANK(M{i}))") for i in range(2, len(df_nf) + 2)
        ]

        df_empty = pd.DataFrame(columns=df_m.columns)
        df_empty["ok"] = False

        if os.path.exists(os.path.join(self.root, "v2-dropped.csv")):
            self.df_d = pd.read_csv(os.path.join(self.root, "v2-dropped.csv"))
        else:
            self.df_d = df_empty

        cols = self.get_cols()
        self.df_m = df_m[cols]
        self.df_nf = df_nf[cols]
        self.df_empty = df_empty[cols]
        self.df_sm = self._write_selection_manual(cols)

    def _save(self):
        with ods.writer(os.path.join(self.root, self.OUTPUT_FILENAME)) as odsfile:
            for sheet_name, df in zip(
                [
                    "selection",
                    "selection+manual",
                    "not-found",
                    "not-clear",
                    "not-clear-from-v2",
                ],
                [self.df_m, self.df_empty, self.df_nf, self.df_empty, self.df_d],
            ):
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for i, row in df.fillna("").iterrows():
                    sheet.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v2-cleaned.csv")

    V3SpreadsheetWriter(os.path.join("onboardings", sys.argv[1]))
