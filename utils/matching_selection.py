import pandas as pd


def clean_rows(dataframe):
    wines = dataframe.copy()
    print(f"Total rows: {wines.shape[0]}")

    # price to cents or to zero, if no price
    wines["price"] = wines["price"].fillna(0)

    # show wines with price 0
    wines[wines["price"] == 0]

    # vintage to int or null
    wines["vintage"] = wines["vintage"].fillna(0)
    wines["vintage"] = wines["vintage"].apply(lambda x: int(x))

    # quantity to int or null
    wines["quantity"] = wines["quantity"].fillna(0)
    wines["quantity"] = wines["quantity"].apply(lambda x: int(x))

    if "ok" not in wines.columns:
        wines["ok"] = wines["matched_id"].notnull().astype(int)

    # clean info
    wines = wines[
        [
            "ok",
            "matched_id",
            "external_id",
            "size",
            "vintage",
            "price",
            "info",
#            "storage_area",
            "quantity",
            "internal_notes",
        ]
    ]
    wines = wines.rename(columns={"matched_id": "wine_id"})

    return wines


def generate_insert_file(filenames):
    """Clean wine selection for insertion.

    Parameters
    ----------
    rows : list
        should have parameters:
        - 'matched_id'
        - 'external_id'
        - 'size'
        - 'vintage'
        - 'price'
        - 'info'
        - 'storage_area'
        - 'quantity'
        - 'internal_notes'
    """
    if type(filenames) == str:
        filenames = [filenames]
    dfs = [clean_rows(pd.read_csv(filename)) for filename in filenames]
    wines = pd.concat(dfs, ignore_index=True)

    # matches = pd.read_csv(filenames)
    # wines = clean_rows(matches)

    # matched wines
    selected_wines = wines[wines["ok"] == 1]
    selected_wines = selected_wines.drop(columns=["ok"])
    print(f"Total selected wines: {selected_wines.shape[0]}")
    print()

    # remove duplicates
    winesWithValidVintage = selected_wines[selected_wines["vintage"] != 0]
    duplicates = winesWithValidVintage[
        winesWithValidVintage.duplicated(
            subset=["wine_id", "size", "vintage"], keep=False
        )
    ].sort_values(by=["wine_id", "size", "vintage"])

    # net wines are wines without duplicates
    net_wines = selected_wines[~selected_wines.index.isin(duplicates.index)]
    print(f"Total net rows: {net_wines.shape[0]}")

    # Write CSV files
    net_wines.to_csv("v4-insert.csv", index=False)

    if duplicates.shape[0] > 0:
        duplicates.to_csv("v4-insert-duplicates.csv", index=False)

    # mismatched wines
    mismatched_wines = wines[wines["ok"] == 0]
    mismatched_wines = mismatched_wines.drop(columns=["ok"])
    print(f"Total mismatched wines: {mismatched_wines.shape[0]}")
    print()

    # remove duplicates
    winesWithValidVintage = mismatched_wines[mismatched_wines["vintage"] != 0]
    duplicates = winesWithValidVintage[
        winesWithValidVintage.duplicated(
            subset=["wine_id", "size", "vintage"], keep=False
        )
    ].sort_values(by=["wine_id", "size", "vintage"])

    # net wines are wines without duplicates
    net_wines = mismatched_wines[~mismatched_wines.index.isin(duplicates.index)]

    # Write CSV files
    net_wines.to_csv("v4-mismatched.csv", index=False)

    if duplicates.shape[0] > 0:
        duplicates.to_csv("v4-mismatched-duplicates.csv", index=False)
