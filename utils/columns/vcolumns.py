from typing import Union


columns_v2 = {
    "external_id": str,
    "type": str,
    "name": str,
    "winery_name": str,
    "info": str,
    "size": str,
    "vintage": int,
    "price": int,
    "purchase_price": int,
    "quantity": int,
    "storage_area": str,
    "internal_notes": str,
    "visible": bool
}

columns_v3 = {
    "matched_id": str,
    "matched_type": str,
    "matched_name": str,
    "matched_winery_name": str,
    "score": float
}

columns_v5 = {
    "wine_id": str,
    "external_id": str,
    "size": str,
    "vintage": int,
    "price": int,
    "purchase_price": int,
    "info": str,
    "storage_area": str,
    "quantity": int,
    "internal_notes": str,
    "visible": bool
}


class VColumns:
    """Class for getting columns"""

    @classmethod
    def v2(cls, get_types=False) -> Union[dict, list]:
        """Get only v2 columns"""
        if get_types:
            return columns_v2
        return list(columns_v2.keys())

    @classmethod
    def v3(cls, get_types=False) -> Union[dict, list]:
        """Get only v3 columns"""
        if get_types:
            return columns_v3
        return list(columns_v3.keys())

    @classmethod
    def v5(cls, get_types=False) -> Union[dict, list]:
        """Get only v5 columns"""
        if get_types:
            return columns_v5
        return list(columns_v5.keys())

    @classmethod
    def v3_selection(cls, get_types=False) -> Union[dict, list]:
        """v2 and v3 columns with "ok" prepended"""
        res = {"ok": bool, **columns_v2, **columns_v3}
        if get_types:
            return res
        return list(res.keys())

    @classmethod
    def v3_selection_manual(cls, get_types=False) -> Union[dict, list]:
        """v2 columns with "ok" and "matched_id" prepended"""
        res = {"ok": bool, "matched_id": str, **columns_v2}
        if get_types:
            return res
        return list(res.keys())

    @classmethod
    def v3_not_found(cls, get_types=False) -> Union[dict, list]:
        """v2 columns with "ok" and "matched_id" prepended.
        Alias for v3_selection_manual"""
        return cls.v3_selection_manual(get_types)

    @classmethod
    def v45(cls, get_types=False) -> Union[dict, list]:
        """v2 columns with "ok", "matched_id", "matched_type", "matched_name" and "matched_winery_name" prepended"""
        res = {"ok": bool, "matched_id": str, "matched_type": str, "matched_name": str, "matched_winery_name": str, **columns_v2}
        if get_types:
            return res
        return list(res.keys())

    @classmethod
    def all_columns(cls, get_types):
        res = {
            "ok": bool,
            "matched_id": str,
            **columns_v2,
            **columns_v3,
            **columns_v5,
        }
        if get_types:
            return res
        return list(res.keys())
