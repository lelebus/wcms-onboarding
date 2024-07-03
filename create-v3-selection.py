import os
import sys

from utils import V3SpreadsheetWriter


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide the folder containing v2-cleaned.csv")

    V3SpreadsheetWriter(os.path.join("onboardings", sys.argv[1]))
    print(f"Created {sys.argv[1]}/v3-selection-draft.ods")
