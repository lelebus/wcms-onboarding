import sys
import urllib3

from dotenv import load_dotenv
from matching_alg import create_matches
from urllib3.exceptions import InsecureRequestWarning

if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) != 2:
        raise ValueError("Please provide the path to the cleaned CSV file")

    urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings
    create_matches(sys.argv[1], "v2-cleaned.csv")
