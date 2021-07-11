# LaTAR Processing

Python script used for processing JSON files collected by LaTAR Bot. Current features:

- Creates one CSV file per Objective per Session, named based on phone, objective, period, and repetitions
- Aligns rows for each objective such that:
  - stimulus time must be less than response time
  - current response time must be < next stimulus time
- Simple, folder-based input/output for batches processing

Note: Be careful that the same phone/objective/period/repetition combo results in an overwrite! No feature to merge CSVs yet.

## Setup

The `laTAR_parser.py` Python script requires `python3` (download from https://www.python.org/downloads/) and the Python packages listed in `requirements.txt`.

To install the required Python packages, either:

- Run the `install.sh` script with `./install.sh` on Mac or Linux
- In a terminal/command prompt, run `python3 -m pip install -r requirements.txt`. If it fails due to insufficient permissions, add `--user` at the end.

## Usage

1. Place all .json files in the `01-JSON_data/` folder
2. Run the `laTAR_parser.py` script

    ```
    python3 laTAR_parser.py
    ```

    Some customizations that can be set in the Python script:
    
    - Set whether .csv files are overwritten by setting `IGNORE_OVERWRITE` to True (always overwrite) or False (ask before overwriting)
    - Where the input/output folders are with `INPUT_JSON_DIR` and `OUTPUT_CSV_DIR`

3. Grab results from the `02-CSV_data/` folder.
