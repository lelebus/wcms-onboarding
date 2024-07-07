# Getting started: Installation
The necessary Python modules to make the onboarding work are in `requirements.txt`.

It is highly recommended to use virtual environments, in order not to pollute your system Python installation.
To do this, you can use either `venv` or `conda`.

### Create virtual environments with venv
First, create a local `venv` virtual environment:
```bash
python3 -m venv venv
```
This will create a folder called `venv` in your working directory.

Note: If `venv` is not installed on your local machine, you can install it using your system package manager.

After you created the virtual environment, you must activate it:
```bash
source venv/bin/activate
```

You can now install the necessary Python modules:
```bash
pip install -r requirements.txt
```
Note: make sure to run this command within your virtual environment only,
otherwise the packages will be installed on your system Python installation,
which is not recommended.

If you wish to exit from the virtual environment, run:
```bash
deactivate
```
If you wish to delete the virtual environment, just remove the `venv` folder.

### Create virtual environments with conda
As an alternative, you can use `conda` to manage your virtual environments
You can check the [docs](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for how to do it.


# Onboarding procedure
The onboarding is a semi-automatized process, where a matching algorithm tries to match the wines provided by the client with the wines in our database. Some manual data cleaning and checks are necessary.

## Pipeline overview
![image](resources/onboarding_pipeline.jpg)


This table provides an overview of the purpose and formatting of all the intermediate files. More details can be found below.

| Name                     | Description                                                                |
| ------------------------ | -------------------------------------------------------------------------- |
| `v0-original`            | Raw input file from the client. Usually docx or xlsx.                      |
| `v1-start`               | input file in txt or csv format.                                           |
| `v2-dropped.csv`         | Wines where formatting is too messy. Will be a tab in `v5-forward.ods`     |
| `v2-cleaned.csv`         | Input File with formatted headers and content. Used to find matches in DB. |
| `v3-selection-draft.ods` | Wines matched with the DB, matches must be manually checked.               |
| `v3-selection.ods`       | Manual check of the matches done.                                          |
| `v4-matches-draft.ods`   | Wines that were matches wrongly, where ids must be inserted manually.      |
| `v4-matches.ods`         | Wines with where all the matches manually checked and ids added.           |
| `v5-insert.csv`          | File formatted for insertion.                                              |
| `v5-forward.ods`         | Wines where ids were not found, to forward to the client                   |

## Detailed steps
### Getting started
First, switch to the `main` branch and git pull to ensure that you are up to date with the latest changes:
```bash
git checkout main
git pull
```

Create a dedicated git branch for the onboarding of each client. Execute the following command to create and switch to this branch:
```bash
git checkout -b onboarding/<CLIENT_NAME>
```

**IMPORTANT**:
 - Ensure you commit your changes to the onboarding branch after completing each of the subsequent steps.
 - Only merge the onboarding branch into `main` once you have finished all the steps.

### v0-original: Beginning of the onboarding
 - Create the onboarding folder `onboardings/<CLIENT NAME>`.
 - Put the file provided by the client in the onboarding folder, name it `v0-original` and keep the file extension unchanged.
 - Commit your changes.

### v1-start.csv (.txt): true input file
This file contains the contents of `v0-original`, but converted in a more machine-friendly format.

If `v0-original` is a spreadsheet (`.xlsx`, `.ods` or similar), `v1-start` should be a `.csv` file.
Otherwise, it should be a `.txt` file.

Some manual cleanup of `v1-start` may be performed if deemed necessary.


### v2-cleaned.csv
Create a notebook in the

Contents must be formatted so that these types are respected:
| Field name       | dtype | meaning                            |
| ---------------- | ----- | ---------------------------------- |
| `external_id`    | `str` | unique id to easily identify wines |
| `type`           | `str` | wine type (RED, WHITE etc.)        |
| `name`           | `str` | name of the wine                   |
| `winery_name`    | `str` | name of the winery                 |
| `info`           | `str` | extra information                  |
| `size`           | `str` | bottle format                      |
| `vintage`        | `int` | vintage year                       |
| `price`          | `int` | price in **cents**                 |
| `purchase_price` | `int` | purchase price in **cents**        |
| `quantity`       | `int` | number of bottles present          |
| `storage_area`   | `str` | storage area of the wines          |
| `internal_notes` | `str` | internal notes for the wine        |

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
The onbarding procedure was different for these restaurants:
 - damichele
 - dolomiti-lodge-alvera
 - laite
 - mondschein
 - pfoesl
 - vinessa
 - tivoli-cortina
 - daaurelio
