#!/usr/bin/env python3

"""
find the global minimum
split list in half
find max value in both halves
set the lower max as the baseline
set a sublist between two points
iterate through the list and compute depth from baseline
until the height is equal to baseline, then the end has been reached 
"""

import json
from os import path
import statistics
import matplotlib.pyplot as plt

FILE = "formatted_data"

ALPHABET = ["A","B","C","D","E","F","G","H","I","J","K",
            "L","M","N","O","P","Q","R","S","T","U","V",
            "W","X","Y","Z"]

def process(file):

    with open(file) as json_file:
        data = json.load(json_file)

        # for each region (50 total)
        for i in range(0,50):
            # [for reset on new region]
            area_list = []

            # for each day (reading set) (26 total)
            for j in range(0,26):
                # [for reset on new day]

                window = data["regions"][i]["readings"][j]["reading"]

                # find multiple global minimums (5) and find the largest
                glob_mins = sorted(window)[:5]
                glob_mins_list = []

                # for each candidate lake
                for val in glob_mins:
                    # reset area for each candidate
                    area = 0
                    glob_min_idx = window.index(val)

                    if glob_min_idx == 0 or glob_min_idx == len(window):
                        # assume runoff
                        # ignore that global min
                        continue

                    left_window = window[:glob_min_idx]
                    right_window = window[glob_min_idx:]

                    left_max = max(left_window)
                    right_max = max(right_window)

                    # set baseline as the lower max
                    baseline = min(left_max, right_max)

                    if baseline == left_max:
                        baseline_idx = left_window.index(left_max)
                    else:
                        baseline_idx = right_window.index(right_max) + len(left_window)

                    # baseline is on the RHS
                    if window.index(left_max) < baseline_idx:
                        for k in range(baseline_idx,0,-1):
                            if window[k] <= baseline:
                                area += abs(baseline-window[k])
                            else:
                                break
                    # baseline is on LHS
                    else:
                        for k in range(baseline_idx,200):
                            # append diff of value to baseline
                            # until we hit edge of the great lake
                            if window[k] <= baseline:
                                area += abs(baseline-window[k])
                            else:
                                break

                    # computed candidate lake area
                    # append to sort later
                    glob_mins_list.append(area)

                # select largest candidate lake
                area_list.append(max(glob_mins_list))

            # compute deltas
            if len(area_list) == 0:
                break

            for m in range(1, len(area_list)):
                delta = abs(area_list[m-1] - area_list[m])
                if delta > 1000:
                    # daily change is > 1000
                    print(f"ID {data['regions'][i]['regionID']}, {delta} for {area_list[m-1]} - {area_list[m]}")


            if data['regions'][i]['regionID'] in ["2FEA2A", "E0EB59"]:
                print(area_list)

                
# pay attention to the single instances
process(FILE)

# plots an individual days readings
def plot_readings(file, region_id, reading_id):
    x = list(map(int, range(0,200)))

    with open(file) as json_file:
        data = json.load(json_file)

        # for each region
        for i in range(0,50):
            # for each day
            # identify target region ID
            if data['regions'][i]['regionID'] == region_id:
                for j in range(0,26):
                    # identify reading ID
                    if data['regions'][i]['readings'][j]['readingID'] == reading_id:
                        print(f"regionID-readingID {data['regions'][i]['regionID']}-{data['regions'][i]['readings'][j]['readingID']}")
                        window = data['regions'][i]['readings'][j]['reading']

    print(f"min of {min(window)} at {window.index(min(window))}, max of {max(window)} at {window.index(max(window))}")


    # find multiple global minimums (5) and find the largest
    glob_mins = sorted(window)[:5]
    print(f"global mins: {glob_mins}")
    glob_mins_list = []

    # for each candidate lake
    count = 1
    for val in glob_mins:
        area = 0
        print("--------")
        print(f"CANDIDATE {count} for global min {val}")
        val_chain = []
        glob_min_idx = window.index(val)

        left_window = window[:glob_min_idx]
        right_window = window[glob_min_idx:]

        left_max = max(left_window)
        right_max = max(right_window)

        # set baseline as the lower max
        baseline = min(left_max, right_max)

        # ensuring correct idx even if there are dupes in window
        if baseline == left_max:
            baseline_idx = left_window.index(left_max)
            print(f"left_max baseline {baseline_idx}")
        else:
            baseline_idx = right_window.index(right_max) + len(left_window)
            print(f"right_max baseline {baseline_idx}")


        print(f"left max {left_max}, right max {right_max}, baseline {baseline} with idx {baseline_idx}")

        # baseline is on the RHS
        if window.index(left_max) < baseline_idx:
            print(f"RHS")
            for k in range(baseline_idx,0,-1):
                if window[k] <= baseline:
                    area += abs(baseline-window[k])
                    val_chain.append(k)
                else:
                    print(f"break at {window[k]} (RHS)")
                    break
        # baseline is on LHS
        else:
            print(f"LHS")
            for k in range(baseline_idx,200):
                # append diff of value to baseline
                # until we hit edge of the great lake
                if window[k] <= baseline:
                    area += abs(baseline-window[k])
                    val_chain.append(k)
                else:
                    print(f"break at {window[k]} (LHS)")
                    break

        # computed candidate lake area
        # append to sort later

        print(f"area {area}")
        print(f"val chain {val_chain}")
        glob_mins_list.append(area)
        count += 1

    print(f"final area {max(glob_mins_list)}")

    plt.plot(x, window)
    plt.savefig(f"{region_id}-{reading_id}.png") 

#plot_readings(FILE, "E0EB59", "M")