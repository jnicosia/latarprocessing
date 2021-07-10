"""
Python program to post-process LaTAR output json file into per-objective CSVs
"""

import json
import pandas as pd
from os.path import exists

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
            print("Discovered new source", source)
            sources[source] = {}

            # Add the first sample
            for key in sample:
                print(" - Adding new key to source", key)
                sources[source][key] = [sample[key]]
    
    return sources

# Given t0 and offset, corrects the time
def correct_time(timestamp, t0, offset):
    return timestamp + t0 - offset

def convert_sources_dict_to_dataframe(sources):
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
        t0_us = data["clockSync"][source_key]["t0"]
        offset_us = data["clockSync"][source_key]["offset"]

        # Save offset and t0 to df
        tempDf["t0_us_" + source_key] = len(tempDf.index) * [t0_us]
        tempDf["offset_us_" + source_key] = len(tempDf.index) * [offset_us]

        # Add columns for corrected time
        for column in tempDf.columns:
            # Process any column with the word "time" in it
            if "time" in column.lower():
                tempDf["corrected_" + column] = correct_time(tempDf[column], t0_us, offset_us)

        # Save dataframe to the source
        source["dataframe"] = tempDf
    
    return sources

# Opening JSON file
filename = 'session_2021-07-10_19-14-39_A30.json'
f = open(filename, 'r')

# returns JSON object as
# a dictionary
data = json.load(f)

# Pull static metadata
phone_name = data["mobile"]["name"]

# Iterating through the json
objectives = data["objectives"]
procedure_objectives = data["procedure"]["objectives"]

# Process each objective
for i,objective in enumerate(objectives):
    # Adds flag in filename
    warning = False

    # Parse json object to per-source dictionaries
    sources = parse_objective_to_sources(objective)
    
    # Convert each source dictionary to dataframe
    sources = convert_sources_dict_to_dataframe(sources)

    # Validate the dataframes
    

    # Merge this objective's dataframes and export as .csv
    source_keys_list = list(sources)
    df = sources[source_keys_list[0]]["dataframe"]

    for source_key in source_keys_list[1:]:
        source = sources[source_key]
        tempDf = source["dataframe"]

        # Make sure sources have same length
        if len(tempDf) != len(df):
            # raise Exception(f"Length mismatch due to source '{source_key}'. Length {str(len(tempDf))} vs {str(len(df))}")
            print(f"WARNING: Length mismatch due to source '{source_key}'. Length {str(len(tempDf))} vs {str(len(df))}")
            warning = True

        df = df.join(tempDf, how='outer')
    
    # Pull metadata from this objective
    typeName = procedure_objectives[i]["typeName"]
    interval = procedure_objectives[i]["parameters"]["interval"]
    count = procedure_objectives[i]["parameters"]["count"]

    csv_filename_elts = [phone_name, typeName, interval, count]
    for i,elt in enumerate(csv_filename_elts):
        csv_filename_elts[i] = str(elt)

    # Export CSV
    csv_filename = "_".join(csv_filename_elts) + ".csv"

    if warning:
        csv_filename = "WARN-" + csv_filename

    if exists(csv_filename):
        val = input(f"WARNING: Output CSV filename '{csv_filename}' already exists! Overwrite? (Y/n): ")
        if val != "Y":
            print("Not overwriting file. Skipping this objective...")
            continue

    df.to_csv(csv_filename)
    print(f"INFO: Successfully wrote '{csv_filename}'")
        

# Closing file
f.close()
