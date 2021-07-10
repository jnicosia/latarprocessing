# Python program to read
# json file

import json
import pandas as pd
from os.path import exists

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

    # Initialize sources
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
    
    # Export this objective as .csv
    source_keys_list = list(sources)
    df = pd.DataFrame.from_dict(sources[source_keys_list[0]])
    df.set_index("index")
    for source_key in source_keys_list[1:]:
        source = sources[source_key]
        tempDf = pd.DataFrame.from_dict(source)
        tempDf.set_index("index")

        # Make sure sources have same length
        if len(tempDf) != len(df):
            # raise Exception(f"Length mismatch due to source '{source_key}'. Length {str(len(tempDf))} vs {str(len(df))}")
            print(f"WARNING: Length mismatch due to source '{source_key}'. Length {str(len(tempDf))} vs {str(len(df))}")
            warning = True

        df = df.join(tempDf, how='outer', rsuffix=source_key)
    
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
