#!/usr/bin/env python3

import json
from os import path

FILE = "formatted_data"

CONTAMINANTS = ["#B48", "#16F", "#C32", "#CEA", "#3F9", "#E48", "#8F5", "#281",
                "#6F3", "#4D4", "#5B9", "#B30", "#B67", "#205", "#E96", "#E46",
                "#C63", "#0B0", "#F04", "#50B", "#C28", "#2C3", "#D3F", "#6BB",
                "#9FB", "#38F", "#E35", "#CBA", "#1C5"]


def decode_binary_data(file):
    """
    decode the original binary input data to ascii
    pipe this to a new file (decoded_data) then use an
    online json formatter and save that as a new file (formatted_data)
    """
    with open(file) as f:
        data = f.read()

    stripped_data = data.replace(" ", "")
    decoded = ''.join(chr(int(stripped_data[i:i+8], 2)) for i in range(0, len(stripped_data), 8))
    return decoded


def read_json(file):
    """
    reads the json data
    """
    with open(file) as json_file:
        data = json.load(json_file)
        total_max = 0

        daily_max = []
        daily_max_ids = []
        for i in range(0,31):
            # iterates day of month (31 days)
            daily_sum = []
            
            for j in range(0,24):
                # iterates hour of the day (24 hours)
                hourly_sum = 0

                for k in range(0, len(data[i]["readings"][j]["contaminants"])):
                    # iterates contaminant IDs (dynamic length)
                    # loop through all contaminant IDs 
                    hourly_sum += data[i]["readings"][j]["contaminants"][CONTAMINANTS[k]] 

                # collect 24 sums for every day
                daily_sum.append(hourly_sum)

            # collects the max of all the sums for every day
            daily_max.append(max(daily_sum))
            # get the id as well
            daily_max_ids.append(data[i]["readings"][daily_sum.index(max(daily_sum))]["id"])

        # collects the max of the daily max
        total_max = max(daily_max)
        total_max_idx = daily_max.index(total_max)
        final_id = daily_max_ids[daily_max.index(total_max)]
        print(f"total max of {total_max} occurs on day {total_max_idx+1} with ID {final_id} which decodes to {bytes.fromhex(final_id).decode('utf-8')}")

#decode_binary_data
#print(decode_binary_data("data"))

# read the json and produce solution
read_json(FILE)