import os
import sys
import pandas as pd

if __name__ == "__main__":
    # Read the CSV file

    # csv_path = os.path.join("onboardings", sys.argv[1], "v2-cleaned.csv")
    df = pd.read_csv("v2-cleaned.csv")

    user_id = "u_01jkz05nty1rgnfgyxjdq17e0p"

    # Generate SQL statements
    sql_statements = []
    for _, row in df.iterrows():
        external_id = row['external_id']
        price = row['takeaway_price']  # Price is already in cents
        
        sql = f"UPDATE user_wines SET take_away_price = {price} WHERE external_id = '{external_id}' AND user_id = '{user_id}';"
        sql_statements.append(sql)

    # Write SQL to file
    # output_path = os.path.join("onboardings", sys.argv[1], "v6-insert_takeaway_prices.sql")
    with open("v6-insert_takeaway_prices.sql", 'w') as f:
        for sql in sql_statements:
            f.write(sql + "\n")
