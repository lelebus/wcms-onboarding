import os
import sys
import urllib3

from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning

from utils import V45SpreadsheetWriter


if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v2-cleaned.csv")
    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

    V45SpreadsheetWriter(os.path.join("onboardings", sys.argv[1]))
