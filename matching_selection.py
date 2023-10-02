import pandas as pd


def clean_matches(dataframe):
    print(f'Total rows: {dataframe.shape[0]}')

    dataframe.head()

    # take only correct matches
    wines = dataframe[dataframe['ok'] == 1]
    print(f'Total selected wines: {wines.shape[0]}')
    print()

    # price to cents or to zero, if no price
    wines['price'] = wines['price'].fillna(0)
    wines['price'] = wines['price'].apply(lambda x: int(x) * 100)

    # show wines with price 0
    wines[wines['price'] == 0]

    # vintage to int or null
    wines['vintage'] = wines['vintage'].fillna(0)
    wines['vintage'] = wines['vintage'].apply(lambda x: int(x))

    # clean info
    wines = wines[['matched_id', 'size', 'vintage',
                   'price', 'info', 'area', 'internal_notes']]
    wines = wines.rename(columns={'matched_id': 'wine_id'})

    return wines


def generate_insert_file(filename):
    """Clean wine selection for insertion.

    Parameters
    ----------
    rows : list
        should have parameters:
        - 'matched_id'
        - 'size'
        - 'vintage'
        - 'price'
        - 'info'
        - 'area'
        - 'internal_notes'
    """
    matches = pd.read_csv(filename)
    wines = clean_matches(matches)

    # remove duplicates
    vintageNoNaWines = wines[wines['vintage'].notna()]
    duplicates = vintageNoNaWines[vintageNoNaWines.duplicated(
        subset=['wine_id', 'size', 'vintage'], keep=False)].sort_values(by=['wine_id', 'size', 'vintage'])
    net_wines = wines.drop_duplicates(
        subset=['wine_id', 'size', 'vintage'], keep=False)

    print(f'Total net rows: {net_wines.shape[0]}')

    # Write CSV files
    net_wines.to_csv('v4-insert.csv', index=False)

    if duplicates.shape[0] > 0:
        duplicates.to_csv('v4-duplicates.csv', index=False)
