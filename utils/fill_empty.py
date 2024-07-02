from utils import VColumns


default_values = {
    str: "",
    int: 0,
    float: 0.0,
    bool: False,
}


def fill_empty(df, columns):
    df = df.copy()
    for column in columns:
        if column not in df.columns:
            df[column] = default_values[VColumns.all_columns(get_types=True)[column]]
    return df[columns]
