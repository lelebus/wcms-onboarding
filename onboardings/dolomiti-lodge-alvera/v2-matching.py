# %% [markdown]
# # Run matching algorithm
# 
# One the data has been cleaned, prepared, and the content of the new winelist has been used to obtain further information, we proceed with the matching.

# %%
import sys
sys.path.append('..')

import matching_alg as alg

alg.create_matches('v2-cleaned.csv')

# %%
