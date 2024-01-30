import pandas as pd
from queries import query_es_clean


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
    for row in rows:
        search_name = row['name']
        search_winery = row['winery_name']
        search_type = row['type']

        d = {
            'external_id': row['external_id'],
            'name': search_name,
            'winery_name': search_winery,
            'type': row['type'],
            'storage_area': row['storage_area'],
            'size': row['size'],
            'vintage': row['vintage'],
            'price': row['price'],
            'info': row['info'],
            'quantity': row['quantity'],
            'internal_notes': row['internal_notes'],
            'matched_name': None,
            'matched_winery_name': None,
            'matched_id': None,
            'matched_original_id': None,
            'score': None,
        }

        # add columns for analysis
        try:
            d['expected_id'] = row['expected_id']
            d['failing_info'] = row['failing_info']
        except:
            pass

        # perform search
        match, score = query_es_clean(search_name, search_winery, search_type)
        if match is not None:
            d['matched_name'] = match['name']
            d['matched_winery_name'] = match['winery_name']
            d['type'] = match['type']
            d['matched_id'] = match['id']
            d['score'] = score

            try:
                d['matched_original_id'] = match['original_id']
            except:
                d['matched_original_id'] = None

        matches.append(d)

    return matches


def create_matches(filename):
    # read wines
    wines = pd.read_csv(filename)
    print(f'Total rows: {wines.shape[0]}')
    print()

    # run algorithm
    print('Searching ...', end='\r')
    wines_list = wines.to_dict('records')
    matches_list = search_rows(wines_list)

    # generate new dataframe
    matches = pd.DataFrame(matches_list)
    print(
        f'Total rows: {matches.shape[0]} (should be {wines.shape[0]} - same number of rows as original)')
    print()

    matches = matches[['external_id', 'type', 'name', 'winery_name', 'storage_area',
                       'size', 'vintage', 'price', 'info', 'quantity', 'internal_notes', 'matched_name', 'matched_winery_name',
                       'matched_id', 'matched_original_id', 'score']]
    matches.head()

    # remove not matched rows
    valid_matches = matches[matches['matched_id'].notnull()]
    not_matched = matches[matches['matched_id'].isnull()]

    filename = 'v3-matches.csv'
    valid_matches.to_csv(filename, index=False)

    filename = 'v3-not-found.csv'
    not_matched.to_csv(filename, index=False)

    print(f'Valid matches: {valid_matches.shape[0]}')
    print(f'Not matched: {not_matched.shape[0]}')
    print()
