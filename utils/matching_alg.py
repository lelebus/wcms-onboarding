import os
import json
import requests
import pandas as pd

from utils import VColumns, fill_empty


def prepare_request(url_addition: str) -> dict:
    return {
        "url": os.environ["ELASTICSEARCH_URL"] + "/" + url_addition,
        "headers": {"Content-Type": "application/json"},
    }


def query_es(name, winery_name, wine_type):
    # build query
    conditions = [
        {
            "multi_match": {
                "query": name,
                "fields": ["name"],
                "type": "best_fields",
                "operator": "or",
                "fuzziness": "AUTO",
            }
        },
        {
            "multi_match": {
                "query": winery_name,
                "fields": ["winery.name^2"],
                "type": "best_fields",
                "operator": "or",
                "fuzziness": "1",
            }
        },
    ]

    if wine_type is not None and str(wine_type) != "nan":
        conditions.append({"term": {"type.keyword": wine_type}})

    # perform query
    query = {
        "query": {
            "bool": {
                "must": conditions,
            }
        },
        "size": 1,
    }

    try:
        req_prep = prepare_request("wines/_search")
        response = requests.post(**req_prep, json=query)
        response_json = response.json()
        hits = response_json["hits"]["hits"]

        if len(hits) > 0:
            match = hits[0]["_source"]
            return match, hits[0]["_score"]
        else:
            return None, 0
    except Exception as e:
        print(f"ERROR ({name} - {winery_name})", e)
        return None, 0


def search_rows(rows):
    """Use search algorithm on rows.

    Parameters
    ----------
    rows : list
        should have parameters:
        - 'external_id'
        - 'name'
        - 'winery_name'
        - 'type'
        - 'storage_area'
        - 'size'
        - 'vintage'
        - 'price'
        - 'info'
        - 'quantity'
        - 'internal_notes'

    Returns
    -------
    dataframe : list
    """
    matches = []

    for i, row in enumerate(rows):
        search_name = row["name"] if not pd.isna(row["name"]) else ""
        search_winery = row["winery_name"] if not pd.isna(row["winery_name"]) else ""
        search_type = row["type"] if not pd.isna(row["type"]) else None

        # fill rows
        d = {}
        for k in VColumns.v2():
            d[k] = row[k]
        for k in VColumns.v3():
            d[k] = None

        # add columns for analysis
        try:
            d["expected_id"] = row["expected_id"]
            d["failing_info"] = row["failing_info"]
        except:
            pass

        # perform search
        match, score = query_es(search_name, search_winery, search_type)
        if match is not None:
            d["matched_id"] = match["id"]
            d["matched_type"] = match["type"]
            d["matched_name"] = match["name"]
            d["matched_winery_name"] = match["winery"]["name"]
            d["score"] = score

        matches.append(d)
        print(f"{i+1} of {len(rows)}".ljust(50), end="\r")

    return matches


def create_matches(root):
    # read wines
    wines = pd.read_csv(os.path.join(root, "v2-cleaned.csv"))
    wines = fill_empty(wines, VColumns.v2())
    print(f"Total rows: {wines.shape[0]}")
    print()

    # run algorithm
    print("Searching ...")
    wines_list = wines.to_dict("records")
    matches_list = search_rows(wines_list)

    # generate new dataframe
    matches = pd.DataFrame(matches_list)
    print(
        f"Total rows: {matches.shape[0]} (should be {wines.shape[0]} - same number of rows as original)"
    )
    print()

    matches = matches[VColumns.v2() + VColumns.v3()]

    # remove not matched rows
    valid_matches = matches[matches["matched_id"].notnull()]
    not_matched = matches[matches["matched_id"].isnull()]

    output_path = os.path.join(root, "v3-matches.csv")
    valid_matches.to_csv(output_path, index=False)

    output_path = os.path.join(root, "v3-not-found.csv")
    not_matched.to_csv(output_path, index=False)

    print(f"Valid matches: {valid_matches.shape[0]}")
    print(f"Not matched: {not_matched.shape[0]}")
    print()
