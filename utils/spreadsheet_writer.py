import os
import requests
import pandas as pd
import odswriter as ods

from utils import VColumns, fill_empty
from utils.match_filtering import check_match


def fill_ok_formulas(df):
    return [ods.Formula(f'IF(ISBLANK(B{i}); ""; 1)') for i in range(2, len(df) + 2)]


class V3SpreadsheetWriter:
    OUTPUT_FILENAME = "v3-selection-draft.ods"

    def __init__(self, root, df_valid_matches, df_not_matched):
        self.root = root
        self.df_valid_matches, self.df_not_matched = self._fill_sheets(
            df_valid_matches, df_not_matched
        )
        self._save()

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
        df_valid_matches = fill_empty(df_valid_matches, VColumns.v3_selection(), True)
        df_valid_matches["ok"] = self._fill_ok(df_valid_matches)
        df_valid_matches = df_valid_matches.sort_values("ok", ascending=False)

        df_not_matched = fill_empty(df_not_matched, VColumns.v3_not_found(), True)
        df_not_matched["ok"] = fill_ok_formulas(df_not_matched)

        return df_valid_matches, df_not_matched

    def _save(self):
        print(f"Saving to {os.path.join(self.root, self.OUTPUT_FILENAME)}")
        with ods.writer(os.path.join(self.root, self.OUTPUT_FILENAME)) as odsfile:
            for sheet_name, df in zip(
                ["Auto (select correct)", "Manual (DO NOT TOUCH)"],
                [self.df_valid_matches, self.df_not_matched],
            ):
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for _, row in df.fillna("").iterrows():
                    sheet.writerow(row)


class V4SpreadsheetWriter:
    OUTPUT_FILENAME = "v4-matches-draft.ods"

    def __init__(self, root):
        self.root = root

        self._read_sheets()
        self._save()

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

        df_auto = fill_empty(df_auto, VColumns.v3_selection(), True)
        df_manual = fill_empty(df_manual, VColumns.v3_not_found(), True)

        df_manual["ok"] = fill_ok_formulas(df_manual)
        df_manual["matched_id"] = None

        self.df_auto = df_auto
        self.df_manual = df_manual

    def _save(self):
        print(f"Saving to {os.path.join(self.root, self.OUTPUT_FILENAME)}")
        with ods.writer(os.path.join(self.root, self.OUTPUT_FILENAME)) as odsfile:
            for sheet_name, df in zip(
                ["Auto (DO NOT TOUCH)", "Manual (insert ids)"],
                [self.df_auto, self.df_manual],
            ):
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for _, row in df.fillna("").iterrows():
                    sheet.writerow(row)


def prepare_request(url_addition: str) -> dict:
    return {
        "url": os.environ["ELASTICSEARCH_URL"] + "/" + url_addition,
        "headers": {"Content-Type": "application/json"},
    }


def query_es_by_id_mget(wine_ids: list) -> dict:
    """Query Elasticsearch for a list wine by their IDs.

    Parameters
    ----------
    wine_ids : list
        The ID of the wine to search for

    Returns
    -------
    dict or None
        The wine document if found, None otherwise
    """
    # build query
    docs = [{"_id": wine_id} for wine_id in wine_ids]
    mget_body = {"docs": docs}

    try:
        req_prep = prepare_request("wines/_mget/")
        response = requests.post(**req_prep, json=mget_body)
        response_json = response.json()

        results = []
        for doc in response_json["docs"]:
            if doc.get("found", False):
                results.append(doc["_source"])
            else:
                results.append(None)
        return results

    except Exception as e:
        print(f"ERROR (wine_ids: {wine_ids})", e)
        return None


class V45SpreadsheetWriter:
    OUTPUT_FILENAME = "v4.5-matches-check.ods"

    def __init__(self, root):
        self.root = root

        self._read_sheets()
        self._save()

    def _read_sheets(self):
        df_auto = pd.read_excel(
            os.path.join(self.root, "v4-matches.ods"),
            sheet_name="Auto (DO NOT TOUCH)",
        )
        df_manual = pd.read_excel(
            os.path.join(self.root, "v4-matches.ods"),
            sheet_name="Manual (insert ids)",
        )

        df_manual = fill_empty(df_manual, VColumns.v45(), True)
        df_manual["ok"] = fill_ok_formulas(df_manual)

        matched_info = query_es_by_id_mget(df_manual["matched_id"])
        matched_info = pd.Series(matched_info)

        df_manual["matched_type"] = matched_info.apply(lambda x: x["type"] if x else None)
        df_manual["matched_name"] = matched_info.apply(lambda x: x["name"] if x else None)
        df_manual["matched_winery_name"] = matched_info.apply(lambda x: x["winery"]["name"] if x else None)

        self.df_auto = df_auto
        self.df_manual = df_manual

    def _save(self):
        print(f"Saving to {os.path.join(self.root, self.OUTPUT_FILENAME)}")
        with ods.writer(os.path.join(self.root, self.OUTPUT_FILENAME)) as odsfile:
            for sheet_name, df in zip(
                ["Auto (DO NOT TOUCH)", "Manual (insert ids)"],
                [self.df_auto, self.df_manual],
            ):
                sheet = odsfile.new_sheet(sheet_name)
                sheet.writerow(df.columns)
                for _, row in df.fillna("").iterrows():
                    sheet.writerow(row)
