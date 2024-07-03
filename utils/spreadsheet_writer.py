import os
import pandas as pd
import odswriter as ods

from utils import VColumns, fill_empty
from utils.match_filtering import check_match


class MySheet(ods.Sheet):
    def __init__(self, dom, name="Sheet 1", cols=None):
        super().__init__(dom, name, cols)
        self.name = name

    def writerows(self, rows):
        """Override the writerows method to add conditional formatting to the sheet.
        The conditional formatting makes the rows green if the value in column A is 1.
        """
        super().writerows(rows)
        conditional_formats = self.dom.createElement("calcext:conditional-formats")

        conditional_format = self.dom.createElement("calcext:conditional-format")
        conditional_format.setAttribute(
            "calcext:target-range-address", f"'{self.name}.A1:'{self.name}.R1048576'"
        )
        condition = self.dom.createElement("calcext:condition")
        condition.setAttribute("calcext:apply-style-name", "Good")
        condition.setAttribute("calcext:value", "formula-is([.$A1]=1)")
        condition.setAttribute("calcext:base-cell-address", f"{self.name}.A1")

        conditional_format.appendChild(condition)
        conditional_formats.appendChild(conditional_format)
        self.table.appendChild(conditional_formats)


class MyOdsWriter(ods.ODSWriter):
    def new_sheet(self, name=None, cols=None):
        """
        Create a new sheet in the spreadsheet and return it so content can be added.
        :param name: Optional name for the sheet.
        :param cols: Specify the number of columns, needed for compatibility in some cases
        :return: Sheet object
        """
        sheet = MySheet(self.dom, name, cols)
        self.sheets.append(sheet)
        return sheet


def fill_ok_formulas(df):
    return [ods.Formula(f'IF(ISBLANK(B{i}); ""; 1)') for i in range(2, len(df) + 2)]


class BaseSpreadsheetWriter:
    def __init__(self, root, OUTPUT_FILENAME):
        self.root = root
        self.OUTPUT_FILENAME = OUTPUT_FILENAME

    # TODO: make this work
    # Should be achievable by inserting the contents
    # of resources/styles.xml in the zip file
    @staticmethod
    def write_conditional_formatting(sheet):
        conditional_formats = sheet.dom.createElement("calcext:conditional-formats")

        conditional_format = sheet.dom.createElement("calcext:conditional-format")
        conditional_format.setAttribute(
            "calcext:target-range-address", f"'{sheet.name}.A1:'{sheet.name}.R1048576'"
        )
        condition = sheet.dom.createElement("calcext:condition")
        condition.setAttribute("calcext:apply-style-name", "Good")
        condition.setAttribute("calcext:value", "formula-is([.$A1]=1)")
        condition.setAttribute("calcext:base-cell-address", f"{sheet.name}.A1")

        conditional_format.appendChild(condition)
        conditional_formats.appendChild(conditional_format)
        sheet.table.appendChild(conditional_formats)

    def save(self, sheet_names, dfs):
        with MyOdsWriter(os.path.join(self.root, self.OUTPUT_FILENAME)) as odsfile:
            for sheet_name, df in zip(sheet_names, dfs):
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for _, row in df.fillna("").iterrows():
                    sheet.writerow(row)
                self.write_conditional_formatting(sheet)
        print(f"Saved to {os.path.join(self.root, self.OUTPUT_FILENAME)}")


class V3SpreadsheetWriter:
    OUTPUT_FILENAME = "v3-selection-draft.ods"

    def __init__(self, root, df_valid_matches, df_not_matched):
        self.root = root
        self.df_valid_matches, self.df_not_matched = self._fill_sheets(
            df_valid_matches, df_not_matched
        )
        self.save()

    @classmethod
    def _fill_ok(cls, df):
        """To be modified for finding sure matches"""
        to_fill = []
        for _, row in df.iterrows():
            is_exact = check_match(
                row["name"],
                row["winery_name"],
                row["type"],
                row["matched_name"],
                row["matched_winery_name"],
                row["matched_type"],
            )
            to_fill.append(is_exact)

        print(f"Found {sum(to_fill)} exact matches")
        return [1 if el else None for el in to_fill]

    def _fill_sheets(self, df_valid_matches, df_not_matched):
        df_valid_matches = fill_empty(df_valid_matches, VColumns.v3_selection())
        df_valid_matches["ok"] = self._fill_ok(df_valid_matches)
        df_valid_matches = df_valid_matches.sort_values("ok", ascending=False)

        df_not_matched = fill_empty(df_not_matched, VColumns.v3_not_found())
        df_not_matched["ok"] = fill_ok_formulas(df_not_matched)

        return df_valid_matches, df_not_matched

    def save(self):
        super().save(
            ["Auto (select correct)", "Manual (DO NOT TOUCH)"],
            [self.df_valid_matches, self.df_not_matched],
        )


class V4SpreadsheetWriter(BaseSpreadsheetWriter):
    OUTPUT_FILENAME = "v4-matches-draft.ods"

    def __init__(self, root):
        self.root = root

        self._read_sheets()
        self.save()

    def _read_sheets(self):
        df_selection = pd.read_excel(
            os.path.join(self.root, "v3-selection.ods"),
            sheet_name="Auto (select correct)",
        )
        df_not_matched = pd.read_excel(
            os.path.join(self.root, "v3-selection.ods"),
            sheet_name="Manual (DO NOT TOUCH)",
        )

        matches_mask = df_selection["ok"].apply(lambda x: x in (1, True))

        df_auto = df_selection.loc[matches_mask].copy()
        df_manual = df_selection.loc[~matches_mask].copy()
        df_manual = pd.concat([df_not_matched, df_manual])

        df_manual["ok"] = fill_ok_formulas(df_manual)
        df_manual["matched_id"] = None

        self.df_auto = fill_empty(df_auto, VColumns.v3_selection())
        self.df_manual = fill_empty(df_manual, VColumns.v3_not_found())

    def save(self):
        super().save(
            ["Auto (DO NOT TOUCH)", "Manual (insert ids)"],
            [self.df_auto, self.df_manual],
        )
