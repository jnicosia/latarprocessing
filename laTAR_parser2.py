"""
Python program to post-process LaTAR output json file into per-objective CSVs
"""

import json
import pandas as pd
import numpy as np
import os
from os.path import exists, normpath

# Path to input JSON files
INPUT_JSON_DIR = "./03-JSON_data"
OUTPUT_CSV_DIR = "./04-CSV_data"

# True to prompt before overwriting, False to simply overwrite
IGNORE_OVERWRITE = True

# Definitions
STIMULUS = 0
RESPONSE = 1
SOURCE = 2
COLUMN = 4
LABEL = 5

# Debug print
DEBUG = False

# Definitions for merging fixture and mobile data
# - Must place the primary pair ("real" latency) pair first. longer/secondary latency should appear after the first
TYPENAME_STIMULUS_RESPONSE = {
    "Display Latency" : [
        # Primary latency
        {
            LABEL: "display_latency_us",
            STIMULUS: {
                SOURCE: "mobile",
                COLUMN: "corrected_displayTime_mobile",
            },
            RESPONSE: {
                SOURCE: "fixture",
                COLUMN: "corrected_detectTime_fixture",
            },
        },
        # Seconary latencies
        {
            LABEL: "callback_latency_us",
            STIMULUS: {
                SOURCE: "mobile",
                COLUMN: "corrected_callbackTime_mobile",
            },
            RESPONSE: {
                SOURCE: "fixture",
                COLUMN: "corrected_detectTime_fixture",
            },
        },
    ],
    "Capacitive Tap Latency" : [
        # Primary latency
        {
            LABEL: "action_latency_us",
            STIMULUS: {
                SOURCE: "fixture",
                COLUMN: "corrected_timestamp_fixture",
            },
            RESPONSE: {
                SOURCE: "mobile",
                COLUMN: "corrected_actionTime_mobile",
            },
        },
        # Seconary latencies
        {
            LABEL: "callback_latency_us",
            STIMULUS: {
                SOURCE: "fixture",
                COLUMN: "corrected_timestamp_fixture",
            },
            RESPONSE: {
                SOURCE: "mobile",
                COLUMN: "corrected_callbackTime_mobile",
            },
        },
    ],
    "Solenoid Tap Latency" : [
        # Primary latency
        {
            LABEL: "action_latency_us",
            STIMULUS: {
                SOURCE: "fixture",
                COLUMN: "corrected_timestamp_fixture",
            },
            RESPONSE: {
                SOURCE: "mobile",
                COLUMN: "corrected_callbackTime_mobile",
            },
        },
        # Seconary latencies
        {
            LABEL: "callback_latency_us",
            STIMULUS: {
                SOURCE: "fixture",
                COLUMN: "corrected_timestamp_fixture",
            },
            RESPONSE: {
                SOURCE: "mobile",
                COLUMN: "corrected_actionTime_mobile",
            },
        },
    ],
}

# Debug print
def dprint(s):
    if DEBUG:
        print("DEBUG: " + str(s))

def parse_objective_to_sources(objective):
    sources = {}

    for sample in objective["data"]:
        # Build dataframe
        source = sample["source"]
        if source in sources:
            # Already have this source
            for key in sample:
                sources[source][key] += [sample[key]]
        else:
            # Initialize source
            dprint(f"Discovered new source '{source}'")
            sources[source] = {}

            # Add the first sample
            for key in sample:
                dprint(f" - Adding new key to source '{key}'")
                sources[source][key] = [sample[key]]

    return sources

# Given t0 and offset, corrects the time
def correct_time(timestamp, t0, offset):
    return timestamp + t0 - offset

def convert_sources_dicts_to_dataframes(json_data, sources):
    dataframes = {}
    source_keys_list = list(sources)

    for source_key in source_keys_list:
        source = sources[source_key]
        tempDf = pd.DataFrame.from_dict(source)

        # tempDf.set_index("index") # Index could be offset later during validation, so don't index off of it

        # Delete source column
        tempDf.pop('source')

        # Append suffix to all columns
        tempDf = tempDf.add_suffix("_" + source_key)

        # Pull time parameters for this column
        t0_us = json_data["clockSync"][source_key]["t0"]
        offset_us = json_data["clockSync"][source_key]["offset"]

        # Save offset and t0 to df
        tempDf["t0_us_" + source_key] = len(tempDf.index) * [t0_us]
        tempDf["offset_us_" + source_key] = len(tempDf.index) * [offset_us]

        # Add columns for corrected time
        for column in tempDf.columns:
            # Process any column with the word "time" in it
            if "time" in column.lower():
                tempDf["corrected_" + column] = correct_time(tempDf[column], t0_us, offset_us)

        # Save dataframe to the source
        dataframes[source_key] = tempDf

    return dataframes

# Inserts a row of NaNs at the specified row index
def insert_df_row(df, row_idx):
    pre_df = df.iloc[:row_idx]
    na_row = pd.DataFrame([[np.nan]*len(df.iloc[0])], columns=list(df))
    na_row.index = range(row_idx, row_idx + 1)
    post_df = df.iloc[row_idx:]
    post_df.index += 1
    return pre_df.append(na_row).append(post_df)

# For a stimulus and response to be aligned:
# - stimulus must be <= response timestamp (increment response until satisfied)
# - response timestamp must be < next stimulus timestamp (increment stimulus until satisfied)
def align_dataframes(dataframes, typeName):
    # Determine source and destination columns based on objective type
    stimulus = TYPENAME_STIMULUS_RESPONSE[typeName][0][STIMULUS]
    response = TYPENAME_STIMULUS_RESPONSE[typeName][0][RESPONSE]

    # Initialize stimulus pointer to first index
    row_idx = 0

    while row_idx < len(dataframes[stimulus[SOURCE]]) and row_idx < len(dataframes[response[SOURCE]]):
        # Insert rows in stimulus before row_idx so stimulus < response
        while (
            row_idx < len(dataframes[stimulus[SOURCE]]) and
            row_idx < len(dataframes[response[SOURCE]]) and
            dataframes[stimulus[SOURCE]].iloc[row_idx][stimulus[COLUMN]] > dataframes[response[SOURCE]].iloc[row_idx][response[COLUMN]]
        ):
            dprint("WARN: Stimulus > response. Inserting row before stimulus at index {row_idx}")
            dataframes[stimulus[SOURCE]] = insert_df_row(dataframes[stimulus[SOURCE]], row_idx)
            row_idx += 1
            dprint(f"  new row idx: {row_idx}")

        # Insert rows in response before row_idx so response < next stimulus
        while (
            ((row_idx + 1) < len(dataframes[stimulus[SOURCE]])) and
            (row_idx < len(dataframes[response[SOURCE]])) and
            (dataframes[response[SOURCE]].iloc[row_idx][response[COLUMN]] > dataframes[stimulus[SOURCE]].iloc[row_idx + 1][stimulus[COLUMN]])
        ):
            print(f"WARN: Response > next stimulus. Inserting row before response at index {row_idx}")
            dataframes[response[SOURCE]] = insert_df_row(dataframes[response[SOURCE]], row_idx)
            row_idx += 1
            dprint(f"  new stim idx: {row_idx}  new resp idx: {row_idx}")

        if row_idx < len(dataframes[stimulus[SOURCE]]) and row_idx < len(dataframes[response[SOURCE]]):
            dprint(f"Matched pair: stim={dataframes[stimulus[SOURCE]].iloc[row_idx][stimulus[COLUMN]]} resp={dataframes[response[SOURCE]].iloc[row_idx][response[COLUMN]]}")
        row_idx += 1

        dprint(f"  new row idx: {row_idx}")

    # No need to assert this b/c there could be extra rows at end (eg., if stim has no paired response)
    # assert len(dataframes[stimulus[SOURCE]]) == len(dataframes[response[SOURCE]]), "ERROR: at end of validation, stim and resp rows not equal!"

    return dataframes

# Merges dataframes from multiple sources (mobile, fixture, etc)
def merge_source_dataframes(dataframes, typeName):
    # Take the stimulus as the far-left
    source_keys_list = list(dataframes)
    df = dataframes[TYPENAME_STIMULUS_RESPONSE[typeName][0][STIMULUS][SOURCE]]

    for source_key in source_keys_list:
        # Skip the source dataframe when it shows up again
        if source_key == TYPENAME_STIMULUS_RESPONSE[typeName][0][STIMULUS][SOURCE]:
            continue

        # Grab current dataframe from source
        tempDf = dataframes[source_key]

        # Make sure sources have same length
        if len(tempDf) != len(df):
            # raise Exception(f"Length mismatch due to source '{source_key}'. Length {str(len(tempDf))} vs {str(len(df))}")
            print(f"WARN: Length mismatch due to source '{source_key}'. Length {str(len(tempDf))} vs {str(len(df))}")
            #warning = True # Disabled this warning b/c it's not very useful. It's possible to have length mismatch due to missing samples on fixture or mobile

        df = df.join(tempDf, how='outer')

    return df

# Export CSV
seen_files = []

def export_csv(csv_filepath, df):
    global seen_files
    # True if file conflict exists
    conflict = False

    # Uncomment the following to prompt file overwrite if it exists
    if exists(csv_filepath) and (csv_filepath not in seen_files):
        print("**********************************************************")
        print(f"WARN: Output CSV filename '{csv_filepath}' already exists!")
        print("**********************************************************")
        conflict = True
        if not IGNORE_OVERWRITE:
            val = input(f"Overwrite CSV? (Y/n): ")
            if val != "Y":
                print("Not overwriting file. Skipping this objective...")
                return conflict

    try:
        # Only overwrite the first time we see a file, otherwise append
        if csv_filepath not in seen_files:
            df.to_csv(csv_filepath, index=False)
            seen_files.append(csv_filepath)
        else:
            df.to_csv(csv_filepath, index=False, mode='a', header=False)
        print(f"INFO: Successfully wrote '{csv_filepath}'")
        return conflict
    except Exception as e:
        print(f"ERROR: Failed to write to '{csv_filepath}': {str(e)}")
        return True

#######################################################

# Processes a JSON file and returns the number of failures
def process_file(filename, output_dir):
    print(f"INFO: Processing file '{filename}'...")

    f = open(filename, 'r')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Close file
    f.close()

    # Pull static metadata
    phone_name = data["mobile"]["name"]

    # Iterating through the json
    objectives = data["objectives"]
    procedure_objectives = data["procedure"]["objectives"]

    conflicts = 0

    # Process each objective
    for i,objective in enumerate(objectives):
        # Adds flag in filename
        warning = False

        # Pull metadata from this objective
        typeName = procedure_objectives[i]["typeName"]
        interval = procedure_objectives[i]["parameters"]["interval"]
        count = procedure_objectives[i]["parameters"]["count"]
        load_name = procedure_objectives[i]["parameters"]["load"]

        # Replace empty strings with "none" for load name
        load_name = load_name if load_name != "" else "none"

        print(f"INFO: Processing objective '{typeName}'")

        # Parse json object to per-source dictionaries
        sources = parse_objective_to_sources(objective)

        # Convert each source dictionary to dataframe
        dataframes = convert_sources_dicts_to_dataframes(data, sources)

        # Align rows between stimulus and response dataframes
        dataframes = align_dataframes(dataframes, typeName)

        # Merge this objective's dataframes and export as .csv
        df = merge_source_dataframes(dataframes, typeName)

        # add latency (difference between stimulus and response values)
        for stim_resp in TYPENAME_STIMULUS_RESPONSE[typeName]:
            df[stim_resp[LABEL]] = df[stim_resp[RESPONSE][COLUMN]] - df[stim_resp[STIMULUS][COLUMN]]

        # Add metadata as new columns
        df["phone_model"] = len(df.index) * [phone_name]
        df["load"] = len(df.index) * [load_name]

        # Make sure all elements used in output CSV filename are strings
        csv_filename_elts = [phone_name, typeName, interval, "ms", count, "x"]
        for i,elt in enumerate(csv_filename_elts):
            csv_filename_elts[i] = str(elt)

        # Export CSV
        csv_filename = ("_".join(csv_filename_elts) + ".csv").replace(" ", "_")

        if warning:
            csv_filename = "WARN-" + csv_filename

        csv_folder = normpath(output_dir + "/" + typeName.replace(" ", "_"))
        csv_filepath = normpath(csv_folder + "/" + csv_filename)

        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        if export_csv(csv_filepath, df):
            conflicts += 1

    return conflicts

#######################################################
# Main program
#######################################################

files = os.listdir(normpath(INPUT_JSON_DIR))
conflicts = 0
num_processed_files = 0

for i,file in enumerate(files):
    print(f"========[{i}/{len(files)}]=======")
    filepath = normpath(INPUT_JSON_DIR + "/" + file)

    if file.endswith(".json"):
        conflicts += process_file(filepath, OUTPUT_CSV_DIR)
        num_processed_files += 1
    else:
        print(f"INFO: Ignoring non-json file '{filepath}'")

print(f"\n\nINFO: Done. Processed {num_processed_files} JSON files with {conflicts} conflicts/failures.")
if conflicts > 0:
    print("See 'WARN' flags in log output above to see what went wrong. Conflicts are when the output file already exists.")
