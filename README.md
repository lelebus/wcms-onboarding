# Onboarding procedure

## Pipeline
The onboarding phase follows this pipeline:
![image](resources/onboarding_pipeline.jpg)

## Intermediate files

### Overview
This table provides an overview of the purpose and formatting of the documents of each onboarding.

TODO: write spec for `v3-selection.csv` files.

| Name                           | Description                                                                    | Purpose   |
| ------------------------------ | ------------------------------------------------------------------------------ | --------- |
| `v0-original`                  | Raw input file from the client.                                                | input     |
| `v1-cleaned.csv`               | Input file with formatted headers.                                             | input     |
| `v2-dropped.csv`               | Input File with formatted headers and content. Used to add wines manually.     | input     |
| `v2-cleaned.csv`               | Input File with formatted headers and content. Used to find matches in DB.     | input     |
| `v3-matches-sure.csv`          | Wines matched automatically with the DB. No further check.                     | matches   |
| `v3-matches.csv`               | Wines matched automatically with the DB. Manual check needed.                  | matches   |
| `v3-not-found.csv`             | Wines not successfully matched automatically with the DB. Manual check needed. | matches   |
| `v3-selection.csv`             | Matches manually confirmed to be correct                                       | matches   |
| `v3-selection-not-found.csv`   | Wines not successfully matched manually.                                       | matches   |
| `v3-selection+manual.csv`      | Wines matched manually with the DB.                                            | matches   |
| `v4-insert.csv`                | Wines to be inserted in `user_wines`.                                          | insertion |
| `v4-insert-duplicates.csv`     | Duplicates of wines in `v4-insert.csv`.                                        | info      |
| `v4-mismatched.csv`            | Wines in `v3-matches.csv` that were matched wrongly.                           | info      |
| `v4-mismatched-duplicates.csv` | Wines to be inserted in `user_wines`.                                          | info      |

## Content description
This section gives an overview on the formatting standards for headers and contents of the intermediate files.

### v1
The file `v1-cleaned.csv` has the same contents as `v0-original`. The difference is in the fields, which must be renamed according to the standard specified in `v2`.

Missing fields are ignored.

It might be the case that 2 original fields must be joined in order to be mapped to one of the standard fields. In that case, fields get the suffixes `_one`, `_two` etc.


### v2
Contents must be formatted so that these types are respected:
| Field name       | dtype | meaning                            |
| ---------------- | ----- | ---------------------------------- |
| `external_id`    | `str` | unique id to easily identify wines |
| `name`           | `str` | name of the wine                   |
| `winery_name`    | `str` | name of the winery                 |
| `type`           | `str` | wine type (RED, WHITE etc.)        |
| `storage_area`   | `str` | storage area of the wines          |
| `size`           | `str` | bottle format                      |
| `vintage`        | `int` | vintage year                       |
| `price`          | `int` | price in **cents**                 |
| `purchase_price` | `int` | price in **cents**                 |
| `info`           | `str` | extra information                  |
| `quantity`       | `int` | number of bottles present          |
| `internal_notes` | `str` | internal notes for the wine        |

TODO: align order with `resources/v2-columns.json` and `resources/v3-columns.json`
Important: remove all rows that have a null `name` and/or `winery_name`


The `type` field should always be filled. Most onboarding sheets provided by the customers are divided by type.
This makes it easy to add the type manually.

The possible values for `type` are:
```python
[
    "RED",
    "WHITE",
    "SPARKLING",
    "ROSE",
    "DESSERT"
]
```

The `size` field has only some allowed values. The standard mapping is this:

```python
{
  "HALF_BOTTLE" : 0.375,
  "HALF_LITER" : 0.5,
  "BOTTLE" : 0.75,
  "LITER" : 1,
  "MAGNUM" : 1.5,
  "JEROBOAM" : 3,
  "REHOBOAM" : 4.5,
  "BORDEAUX_JEROBOAM" : 5,
  "MATHUSALEM" : 6,      # default 6l
  "IMPERIAL" : 6,        # alternative name for 6l
  "SALMANAZAR" : 9,
  "BALTHAZAR" : 12,
  "NEBUCHADNEZZAR" : 15,
  "MELCHIOR" : 18,
  "SOLOMON" : 20,
  "SOVEREIGN" : 25,
  "GOLIATH" : 27,
  "MELCHIZEDEK" : 30
}
```
Where the key is the bottle size in liters.

### v3
These files are generated after the automatic matching. In addition to the fields in `v2`, these are added:

| Field name            | dtype   |
| --------------------- | ------- |
| `matched_id`          | `str`   |
| `matched_type`        | `str`   |
| `matched_name`        | `str`   |
| `matched_winery_name` | `str`   |
| `score`               | `float` |

#### v3-selection
The `v3-selection-*` files have also this field added:
| Field name | dtype  |
| ---------- | ------ |
| `ok`       | `bool` |

Which says whether the match is correct or not.


### v4
These files only have these fields:

| Field name       | dtype |
| ---------------- | ----- |
| `wine_id`        | `str` |
| `external_id`    | `str` |
| `size`           | `str` |
| `vintage`        | `int` |
| `price`          | `int` |
| `purchase_price` | `int` |
| `info`           | `str` |
| `storage_area`   | `str` |
| `quantity`       | `int` |
| `internal_notes` | `str` |

`price` and `purchase_price` are expressed in cents.

In the order exactly specified here and in utils/v4-columns.json

## Note for older onboardings
The onbarding procedure was not clearly defined yet for these restaurants:
 - damichele
 - dolomiti-lodge-alvera
 - laite
 - mondschein
 - pfoesl
 - vinessa

Therefore, the onboarding there does not exactly follow the procedure described above.
A major difference is that `v3-matches-sure.csv` is not used. Instead, only `v3-matches-check.csv` is, which is therefore called `v3-matches.csv`.
