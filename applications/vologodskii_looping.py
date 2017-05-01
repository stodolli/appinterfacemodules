"""
    Stefjord Todolli
    April 9, 2017
"""

import argparse
import numpy as np
import subprocess as sys

from chromocaIO.chromoca_parser import write_sim_input_file, parse_epdistance_file


# def chromoca_exe(sim_file):
#     sys.call(["chromoca", sim_file])


def chromoca_ep_eed(snapshot_file):
    parse_option = "--rebuild-protein-frames"
    sys.call(["chromoca_parser", parse_option, snapshot_file],
             stdout = open(snapshot_file.split("/")[0] + "/" + snapshot_file.split("/")[1] + "-proteins.txt", "w"))
    return snapshot_file.split("/")[0] + "/" + snapshot_file.split("/")[1] + "-proteins.txt"


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


def conditional_looping_probability(r0, r1, eeds_list):
    r0_dist = [d for d in eeds_list if d < r0]
    r1_dist = [d for d in eeds_list if d < r1]
    return(len(r0_dist)/len(r1_dist))


def partition_eed_distribution(eeds_list, r0=200):
    eeds = eeds_list.copy()
    eeds.sort()
    lower_bound = r0
    upper_bound = int(np.ceil(eeds[-1]/50 * 1.15)) * 50
    #print(lower_bound, upper_bound)
    limits = []
    lb = lower_bound
    for l in range(lower_bound + 10, upper_bound, 10):
        if conditional_looping_probability(lb, l, eeds) < 0.22:
            limits.append(l)
            lb = l
    if conditional_looping_probability(limits[-1], upper_bound, eeds) > 0.5 and limits[-1] != upper_bound:
        limits[-1] = upper_bound
    else:
        limits.append(upper_bound)
    short_config_eed = np.max([d for d in eeds_list if d<r0])
    short_config_index = eeds_list.index(short_config_eed)
    #print(short_config_index)
    return(short_config_index, limits)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial-eed-file", dest="init_eed_file",
                        help="EP protein distances file from the initial chromatin distribution")
    parser.add_argument("--snapshots-file", dest="snapshots_file",
                        help="File containing configuration snapshots (trajectories) as separate lines.")
    parser.add_argument("--mc-amplitude", dest="mc_amplitude", help="Amplitude to use for MC simulations.")
    #parser.add_argument("--partition-breaks", dest="partition_breaks", nargs = "*",
    #                    help="The breaks to use to partition the eed distributions.")
    args = parser.parse_args()

    r0 = 200
    sim_name_base = args.snapshots_file.split("-mc-")[0]
    log_output = open(sim_name_base.strip("../") + "-epc.log", "w")

    eeds = parse_epdistance_file(args.init_eed_file)
    (init_config_index, limits) = partition_eed_distribution(eeds, r0)
    log_output.write("Limits and estimated probabilities from initial distribution:\n   " + str(limits) + "\n")
    log_output.write("P[{0:1d}|{1:1d}]: ".format(r0, limits[0]))
    log_output.write(str(conditional_looping_probability(r0, limits[0], eeds)) + "\n")
    for i in range(len(limits)-1):
        log_output.write("P[{0:1d}|{1:1d}]: ".format(limits[i], limits[i+1]))
        log_output.write(str(conditional_looping_probability(limits[i], limits[i+1], eeds)) + "\n")
    log_output.write("   Errors:\nP[{0:1d}|{1:1d}]: ".format(r0-25, limits[0]))
    log_output.write(str(conditional_looping_probability(r0-25, limits[0], eeds)) + ";  ")
    log_output.write("P[{0:1d}|{1:1d}]: ".format(r0+25, limits[0]))
    log_output.write(str(conditional_looping_probability(r0+25, limits[0], eeds)) + "\n\n")

    snapshot_file_offsets = get_file_offsets(args.snapshots_file)
    init_config = get_config_snapshot(args.snapshots_file, sim_name_base.strip("../") + "-epc-ini.txt",
                                      init_config_index, snapshot_file_offsets)

    for l in limits:
        sim_name = sim_name_base.strip("../") + "-r{0:04d}--mc1".format(l)
        write_sim_input_file(sim_name_base.strip("../") + "-r{0:04d}--mc1".format(l), 5000000, 200,
                                        init_config, float(args.mc_amplitude), "monovalent_vasily", l)
        #log_output.write("p({0:1d}\{1:1d}): {2:6.5f}".format(init_interval[0], init_interval[1], p) + "\n")
        log_output.write("\nChroMoCa file " + sim_name + " created, starting with " + init_config + " configuration.")
        init_config = sim_name_base.strip("../") + "-r{0:04d}--mc1".format(l) + "/" + sim_name_base.strip("../") +\
                      "-r{0:04d}--mc1_last-snapshot.txt".format(l)
    log_output.close()
