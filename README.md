# Installation
The necessary Python modules to make the onboarding work are in `requirements.txt`.

It is highly recommended to use virtual environments, in order not to pollute your system Python installation.
To do this, you can use either `venv` or `conda`.

### Create virtual environments with venv
First, create a local `venv` virtual environment:
```bash
python3 -m venv venv
```
This will create a folder called `venv` in your working directory.

*Note*: If `venv` is not installed on your local machine, you can install it using your system package manager.

After you create the virtual environment, you must activate it:
```bash
source venv/bin/activate
```
*Note*: when you start a new VScode bash session, the virtual environment is activated automatically

You can now install the necessary Python modules:
```bash
pip install -r requirements.txt
```
*Note*: make **absolutely sure** to run this command within your virtual environment only,
otherwise the packages will be installed on your system Python installation,
which is not recommended.

If you wish to exit from the virtual environment, run:
```bash
deactivate
```

If you wish to delete the virtual environment, just delete the `venv` folder.

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
| `v2-cleaned.csv`         | Input File with formatted headers and content. Used to find matches in DB. |
| `v2-dropped.csv`         | Wines where formatting is too messy. Will be a tab in `v5-forward.ods`     |
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
This is the original file provided by the client.
 - Create the onboarding folder `onboardings/<CLIENT NAME>`.
 - Put the file provided by the client in the onboarding folder, name it `v0-original` and keep the file extension unchanged.
 - it might be the case that you have multiple files from the client. In that case, name them `v0-original-1`, `v0-original-2` etc.
 - Commit your changes:
```bash
git add onboardings/<CLIENT_NAME>/v0-original*
git commit -m "v0: start <CLIENT_NAME> onboarding"
```

### v1-start.csv (.txt): true input file
This file contains the contents of `v0-original`, but in a more machine-friendly format.
 - Copy the contents of `v0-original` in `v1-start`:
   - if `v0-original` is a spreadsheet (`.xlsx`, `.ods` etc.), `v1-start` should be a `.csv` file;
   - if `v0-original` is a document (`.docx`, `.odt` etc.), `v1-start` should be a `.txt` file.
 - Some manual cleanup of `v1-start` may be performed if deemed necessary.
 - If there are multiple `v0-original` files, create also multiple `v1-start` files.
 - Commit your changes
```bash
git add onboardings/<CLIENT_NAME>/v1-start*
git commit -m: "v1: add v1-start"
```

**IMPORTANT**:
 - It might happen that you need to modify `v1-start` while processing it in the next step. In case this happens, commit the changes as you do them:
```bash
git add onboardings/<CLIENT_NAME>/v1-start*
git commit -m: "v1: cleanup v1-start"
```

### v2-cleaned.csv
This is the file that will be given as input to the matching algorithm, so it must be formatted in a standard way.

 - Create a notebook in the onboarding folder, and name it `v1-to-v2.ipynb`. The final output of this notebook should be `v2-cleaned.csv`.
 - Only a single file `v2-cleaned.csv` must exist.
 - Perform all the necessary preprocessing in this notebook. The fields that must be present are shown in the table below.
   - you can use the class `VColumns` in the `utils` module to get the necessary columns
 - Commit your changes
```bash
git add onboardings/<CLIENT_NAME>/v2-cleaned.csv
git commit -m: "v2: add v2-cleaned.csv"
```

Here are all the fields that must be present in `v2-cleaned.csv`:
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

**Important**:
 - no null values should be present. For removing null values, use `fill_empty` from `utils`.
 - if it is not possible to separate `name` and `winery_name`, leave `winery_name` empty and put everything in `name`.

**VERY IMPORTANT!!:**
 - `price` and `purchase_price` must be expressed as an `int` in **cents**, **NOT IN EUR!!**

See more info in the Appendix.


### v3-selection.ods
This file contains the wines matched by the matching algorithm. Some matches need to be checked manually.
 - run the matching script to generate the draft file `v3-selection-draft.ods`
```bash
python generate-v3-selection.py <CLIENT_NAME>
```
 - Commit your changes
```bash
git add onboardings/<CLIENT_NAME>/v3-selection-draft.ods
git commit -m: "v3: add v3-selection-draft.ods"
```
 - create a copy of the draft file, and name it `v3-selection.ods`
 - manually review the matches in the sheet `AUTO (select correct)`
   - put a 1 in the field `ok` if the match is correct, otherwise leave it empty or write 0
 - Commit your changes:
```bash
git add onboardings/<CLIENT_NAME>/v3-selection.ods
git commit -m: "v3: add v3-selection.ods"
```

### v4-matching.ods
This file contains the wines that were marked as not correct in the previous step, as well as the wines that were not matched with any wine in the database.
 - Run the script to generate the draft file `v4-matches-draft.ods`
```bash
python generate-v4-matches.py <CLIENT_NAME>
```
- commit your changes:
```bash
git add onboardings/<CLIENT_NAME>/v4-matches-draft.ods
git commit -m: "v4: add v4-matches-draft.ods"
```
 - Create a copy of the draft file, and name it `v4-matches.ods`.
 - Manually insert `matched_id` in the sheet `Manual (insert id)`:
   - to find the id, search the wine in the admin portal and copy its id;
   - if the wine is not present at all in the database, add it manually. Perform the search again and copy its id.
 - If the wine that needs to be matched is unclear, leave `matched_id` empty.


### v5-insert.csv and v5-forward.ods
 - Run the script to generate the draft files `v5-insert-draft.csv` and `v5-forward-draft.ods`:
```bash
python generate-v5-insert.py <CLIENT_NAME>
```
- commit your changes:
```bash
git add onboardings/<CLIENT_NAME>/v5-insert-draft.csv
git add onboardings/<CLIENT_NAME>/v5-forward-draft.ods
git commit -m: "v5: add v5-insert-draft.ods and v5-forward-draft.ods"
```
 - copy the files and remove `"draft"` from their name
   - they should be fine as they are. If not, perform the necessary manual changes
- commit your changes:
```bash
git add onboardings/<CLIENT_NAME>/v5-insert.csv
git add onboardings/<CLIENT_NAME>/v5-forward.ods
git commit -m: "v5: add v5-insert.ods and v5-forward.ods"
```
 - upload `v5-insert.csv` in the onboarding portal
 - send `v5-forward.csv` to the client for clarification

Congratulations! The onboarding procedure is now complete.

# Appendix
These are details for v2.

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