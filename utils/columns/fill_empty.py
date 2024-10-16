from utils import VColumns


default_values = {
    str: "",
    int: 0,
    float: 0.0,
    bool: 0,  ## IMPORTANT: it might seem wrong to set bool to 0 instead of False, but this is because the values are stored as integers in the spreadsheet
}


# TODO: Explain clearly the purpose of this function and rename it accordingly
def fill_empty(df, columns, reset_columns=False):
    df = df.copy()
    for column in columns:
        if column not in df.columns:
            df[column] = default_values[VColumns.all_columns(get_types=True)[column]]
        try:
            df[column].fillna(
                default_values[VColumns.all_columns(get_types=True)[column]],
                inplace=True,
            )
            df[column] = df[column].astype(VColumns.all_columns(get_types=True)[column])
        except KeyError:
            pass


    if reset_columns:
        return df[columns]
    
    return df


# TODO: Explain clearly the purpose of this function and rename it accordingly
def complete_columns(df, columns):
    df = df.copy()
    for column in columns:
        if column not in df.columns:
            df[column] = default_values[VColumns.all_columns(get_types=True)[column]]
    return df[columns]
