import os
import pandas as pd
import odswriter as ods

from utils import VColumns, fill_empty


class V3SpreadsheetWriterOld:
    OUTPUT_FILENAME = "v3-selection-draft.ods"

    def __init__(self, root):
        self.root = root

        self._read_sheets()
        self._save()

    @classmethod
    def _fill_ok_formulas(cls, df):
        return [ods.Formula(f"NOT(ISBLANK(B{i}))") for i in range(2, len(df) + 2)]

    def _read_sheets(self):
        # selection
        df_s = pd.read_csv(os.path.join(self.root, "v3-matches.csv"))
        df_s["ok"] = False
        self.df_s = fill_empty(df_s, VColumns.v3_selection())  # select and sort columns

        # selection+manual
        df_sm = pd.DataFrame(columns=VColumns.v3_not_found())
        df_sm["ok"] = self._fill_ok_formulas(df_s)
        self.df_sm = fill_empty(df_sm, VColumns.v3_not_found())

        # not-found
        df_nf = pd.read_csv(os.path.join(self.root, "v3-not-found.csv"))
        df_nf["ok"] = self._fill_ok_formulas(df_nf)
        self.df_nf = fill_empty(df_nf, VColumns.v3_not_found())

        # not-clear
        self.df_nc = pd.DataFrame(columns=VColumns.v2())

        # not-clear-from-v2
        if os.path.exists(os.path.join(self.root, "v2-dropped.csv")):
            self.df_nc2 = pd.read_csv(os.path.join(self.root, "v2-dropped.csv"))
        else:
            self.df_nc2 = None

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
                [self.df_s, self.df_sm, self.df_nf, self.df_nc, self.df_nc2],
            ):
                if df is None:
                    continue
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for _, row in df.fillna("").iterrows():
                    sheet.writerow(row)


class V3SpreadsheetWriter:
    OUTPUT_FILENAME = "v3-selection-draft.ods"

    def __init__(self, root, df_valid_matches, df_not_matched):
        self.root = root
        self.df_valid_matches, self.df_not_matched = self._fill_sheets(
            df_valid_matches, df_not_matched
        )
        self._save()

    @classmethod
    def _fill_ok_formulas(cls, df):
        return [ods.Formula(f"NOT(ISBLANK(B{i}))") for i in range(2, len(df) + 2)]

    @classmethod
    def _fill_ok(cls, df):
        """To be modified for finding sure matches"""
        return [False for _ in range(len(df))]

    def _fill_sheets(self, df_valid_matches, df_not_matched):
        df_valid_matches = fill_empty(df_valid_matches, VColumns.v3_selection())
        df_valid_matches["ok"] = self._fill_ok(df_valid_matches)

        df_not_matched = fill_empty(df_not_matched, VColumns.v3_not_found())
        df_not_matched["ok"] = self._fill_ok_formulas(df_not_matched)

        return df_valid_matches, df_not_matched

    def _save(self):
        print(f"Saving to {os.path.join(self.root, self.OUTPUT_FILENAME)}")
        with ods.writer(os.path.join(self.root, self.OUTPUT_FILENAME)) as odsfile:
            for sheet_name, df in zip(
                ["selection", "not-matched (DO NOT TOUCH)"],
                [self.df_valid_matches, self.df_not_matched],
            ):
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for _, row in df.fillna("").iterrows():
                    sheet.writerow(row)
