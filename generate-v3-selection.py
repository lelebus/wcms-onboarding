import os
import sys
import urllib3

from dotenv import load_dotenv
from utils.matching_alg import create_matches
from urllib3.exceptions import InsecureRequestWarning

from utils import V3SpreadsheetWriter

if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v2-cleaned.csv")
    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

    df_valid_matches, df_not_matched = create_matches(
        os.path.join("onboardings", sys.argv[1])
    )

    V3SpreadsheetWriter(
        os.path.join("onboardings", sys.argv[1]), df_valid_matches, df_not_matched
    )
