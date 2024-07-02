# selection.generate_insert_file("daaurelio/v3-selection.csv")
# selection.generate_insert_file("daaurelio/v3-selection-not-found.csv")

import os
import sys
import urllib3

from dotenv import load_dotenv
from matching_alg import create_matches
from urllib3.exceptions import InsecureRequestWarning

import matching_selection as selection

if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v2-cleaned.csv")

    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

    V3_FILENAMES = [
        "v3-selection.csv",
        "v3-selection-not-found.csv",
        "v3-selection+manual.csv",
        "v3-matches-sure.csv",
    ]

    v3_filepaths = [
        os.path.join("onboardings", sys.argv[1], name) for name in V3_FILENAMES
    ]

    selection.generate_insert_file(v3_filepaths)
    # create_matches(sys.argv[1], "v2-cleaned.csv")
