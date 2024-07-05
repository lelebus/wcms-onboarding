import os
import json
from typing import Union


class VColumns:
    """Class for reading columns from files"""

    @classmethod
    def read_columns(cls):
        """Read columns from files"""
        # print("Reading columns...")
        cls.col_mapping = {}
        column_folder = os.path.join(os.environ["PROJECT_ROOT"], "utils", "columns")
        with open(os.path.join(column_folder, "v2.json")) as f:
            cls.col_mapping["v2"] = json.load(f)
        with open(os.path.join(column_folder, "v3.json")) as f:
            cls.col_mapping["v3"] = json.load(f)
        with open(os.path.join(column_folder, "v5.json")) as f:
            cls.col_mapping["v5"] = json.load(f)

    @classmethod
    def get_v(cls, v, get_types) -> Union[dict, list]:
        if not hasattr(cls, "col_mapping"):
            cls.read_columns()

        if get_types:
            type_mapping = {
                "str": str,
                "int": int,
                "float": float,
            }
            return {k: type_mapping[v] for k, v in cls.col_mapping[v].items()}
        else:
            return list(cls.col_mapping[v].keys())

    @classmethod
    def v2(cls, get_types=False) -> Union[dict, list]:
        return cls.get_v("v2", get_types)

    @classmethod
    def v3(cls, get_types=False) -> Union[dict, list]:
        """Columns in v3-columns.json"""
        return cls.get_v("v3", get_types)

    @classmethod
    def v5(cls, get_types=False) -> Union[dict, list]:
        """Get only v5 columns"""
        return cls.get_v("v5", get_types)

    @classmethod
    def v3_selection(cls, get_types=False) -> Union[dict, list]:
        """v2 and v3 columns with "ok" prepended"""
        res = {"ok": bool, **cls.v2(True), **cls.v3(True)}
        if get_types:
            return res
        return list(res.keys())

    @classmethod
    def v3_selection_manual(cls, get_types=False) -> Union[dict, list]:
        """v2 columns with "ok" and "matched_id" prepended"""
        res = {"ok": bool, "matched_id": str, **cls.v2(True)}
        if get_types:
            return res
        return list(res.keys())

    @classmethod
    def v3_not_found(cls, get_types=False) -> Union[dict, list]:
        """v2 columns with "ok" and "matched_id" prepended.
        Alias for v3_selection_manual"""
        return cls.v3_selection_manual(get_types)

    @classmethod
    def all_columns(cls, get_types):
        res = {
            "ok": bool,
            "matched_id": str,
            **cls.v2(True),
            **cls.v3(True),
            **cls.v5(True),
        }
        if get_types:
            return res
        return list(res.keys())
