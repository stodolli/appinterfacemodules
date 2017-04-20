"""
    Stefjord Todolli
    April 9, 2017
"""

import numpy as np
import argparse
import bisect
import subprocess as sys
from chromocaIO.chromoca_parser import write_sim_input_file, parse_eed_file


def chromoca_exe(sim_file):
    sys.call(["chromoca", sim_file])


def chromoca_parser(snapshot_file, parse_option):
    sys.call(["chromoca_parser", parse_option, snapshot_file],
             stdout = open(snapshot_file.split("/")[0] + "/endtoend.txt", "w"))
    return snapshot_file.split("/")[0] + "/endtoend.txt"



def partition_eed(eed_list, r0, breaks=[]):
    """

    :type eed_list: list
    :type r0: int
    :type breaks: list
    :rtype dict
    """
    eed_dist = np.array(eed_list)
    if len(breaks) == 0:
        mean = np.mean(eed_dist)
        stdev = np.std(eed_dist)
        min_eed = np.min(eed_dist)
        max_eed = np.max(eed_dist)
        step = 25 #if mean <= 500 else 50
        l_0 = int(np.floor(min_eed / step) * step)
        l_n = int(np.ceil(max_eed / step) * step)
        midpoint = int(np.ceil((mean - 2*stdev) / step) * step)
        l_breaks = list(range(l_0, r0, step))
        if (midpoint > r0):
            l_breaks.extend(list(range(r0, midpoint, step)))
        else:
            midpoint = r0
        l_breaks.extend(list(range(midpoint, l_n+step, int(np.floor((l_n - midpoint)/3)))))
    else:
        l_breaks = [int(x) for x in breaks]
    l_intervals = [(l_breaks[i], l_breaks[i+1]) for i in range(len(l_breaks)-1)]
    partitioned_eed = dict()
    for l in l_intervals:
        partitioned_eed[l] = []
    dict_keys = sorted(list(partitioned_eed.keys()))
    for i in range(len(eed_dist)):
        key = dict_keys[bisect.bisect(l_breaks, eed_dist[i]) - 1]
        partitioned_eed[key].append((i,eed_dist[i]))
    return partitioned_eed


def get_file_offsets(file_in):
    file_reader = open(file_in)
    offsets = [0]
    while file_reader.readline() != "":
        offsets.append(file_reader.tell())
    return offsets


def get_config_snapshot(snapshots_file, new_snapshot_file, line_n, offsets):
    snapshots_reader = open(snapshots_file)
    snapshots_reader.seek(offsets[line_n])
    n_snapshot = snapshots_reader.readline()
    snapshots_reader.close()
    snapshot_writer = open(new_snapshot_file, "w")
    snapshot_writer.write(n_snapshot)
    snapshot_writer.close()
    return new_snapshot_file


def grab_config_snapshot(snapshots_file, new_snapshot_file, line_n):
    snapshots_reader = open(snapshots_file)
    offsets = [0]
    while snapshots_reader.readline() != "":
        offsets.append(snapshots_reader.tell())
    snapshots_reader.seek(offsets[line_n])
    n_snapshot = snapshots_reader.readline()
    snapshots_reader.close()
    snapshot_writer = open(new_snapshot_file, "w")
    snapshot_writer.write(n_snapshot)
    snapshot_writer.close()
    return new_snapshot_file


def grab_last_snapshot(snapshots_file, new_snapshot_file):
    snapshots_reader = open(snapshots_file)
    offsets = [0]
    i = 0
    while snapshots_reader.readline() != "":
        i += 1
        offsets.append(snapshots_reader.tell())
    snapshots_reader.seek(offsets[i-1])
    n_snapshot = snapshots_reader.readline()
    snapshots_reader.close()
    snapshot_writer = open(new_snapshot_file, "w")
    snapshot_writer.write(n_snapshot)
    snapshot_writer.close()
    return new_snapshot_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial-eed-file", dest="init_eed_file",
                        help="End-to-end distances file from the initial chromatin distribution")
    parser.add_argument("--snapshots-file", dest="snapshots_file",
                        help="File containing configuration snapshots (trajectories) as separate lines.")
    parser.add_argument("--mc-amplitude", dest="mc_amplitude", help="Amplitude to use for MC simulations.")
    parser.add_argument("--partition-breaks", dest="partition_breaks", nargs = "*",
                        help="The breaks to use to partition the eed distributions.")
    args = parser.parse_args()

    eeds = parse_eed_file(args.init_eed_file)
    if args.partition_breaks is None:
        partitioned_eeds = partition_eed(eeds, 200)
    else:
        partitioned_eeds = partition_eed(eeds, 200, args.partition_breaks)

    sim_name_base = args.snapshots_file.split("--")[0]
    init_interval = sorted(partitioned_eeds.keys())[0]
    init_index = sorted(partitioned_eeds[init_interval], key=lambda x: x[1])[0][0]
    snapshot_file_offsets = get_file_offsets(args.snapshots_file)
    init_config = get_config_snapshot(args.snapshots_file,
                                      sim_name_base.strip("../") + "-r{0:03d}".format(init_interval[1]) + "-ini.txt",
                                      init_index, snapshot_file_offsets)
    i = 0
    pdf = []
    log_output = open(sim_name_base.strip("../") + "-epc.log", "w")
    for k in sorted(partitioned_eeds.keys()):
        sim_name = write_sim_input_file(sim_name_base.strip("../") + "-r{0:03d}".format(init_interval[1]),
                             int(np.sqrt(i+1) * 1000000), 200, init_config, init_interval[1], args.mc_amplitude)
        chromoca_exe(sim_name + ".txt")
        # parse output and calculate probabilities
        eed_file = chromoca_parser(sim_name + "/" + sim_name + "_snapshots.txt", "--rebuild-end-to-end")
        eeds = parse_eed_file(eed_file)
        p = len([d for d in eeds if d < init_interval[0]]) / len(eeds)
        pdf.append((init_interval[0], p))
        log_output.write("p({0:1d}\{1:1d}): {2:6.5f}".format(init_interval[0], init_interval[1], p) + "\n")
        i += 1
        if (i >= len(sorted(partitioned_eeds.keys()))):
            break
        init_interval = sorted(partitioned_eeds.keys())[i]
        #init_index = sorted(partitioned_eeds[init_interval], key=lambda x: x[1])[0][0]
        #init_config = get_config_snapshot(args.snapshots_file,
        #                                  sim_name_base.strip("../") + "-r{0:03d}".format(init_interval[1]) + "-ini.txt",
        #                                  init_index, snapshot_file_offsets)
        init_config = grab_last_snapshot(sim_name + "/" + sim_name + "_snapshots.txt",
                                         sim_name_base.strip("../") + "-r{0:03d}".format(init_interval[1]) + "-ini.txt")
    log_output.close()
