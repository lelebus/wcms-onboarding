# %% [markdown]
# # Wines selection to insertion
#
# Load the list of correct matches and generate the import CSV.

# %%
import sys

sys.path.append("..")

import utils.matching_selection as selection

selection.generate_insert_file("v3-selection.csv")

# %%
