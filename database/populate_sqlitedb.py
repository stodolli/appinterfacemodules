"""
    Stefjord Todolli
    Sept 15, 2017
"""

import argparse
import sqlite3 as sq
import numpy as np
from chromocaIO.chromoca_parser import parse_snapshot, parse_eed_file, parse_protein_frames
from utils.structure_properties import radius_gyration, sedimentation_coefficient


def tails_local_to_global_iter(protein_frame, tails_list):
    return(map(lambda x: np.dot(np.array(protein_frame[1]).T, x) + np.array(protein_frame[0]), np.array(tails_list)))


def add_simulation_to_sqlitedb(sqlite_db_file, snapshots_file, sim_setup_file, starting_config_file, log_file,
                               protein_frames_file, endtoend_vectors_file, avg_steps_file):
    # Setup
    db_conn = sq.connect(sqlite_db_file)
    dbc = db_conn.cursor()
    snapshot_reader = open(snapshots_file)
    with open(sim_setup_file) as reader:
        sim_setup = reader.readlines()
    with open(starting_config_file) as reader:
        starting_config = reader.readline().strip()
    with open(log_file) as reader:
        sim_log = reader.readlines()
    with open(protein_frames_file) as reader:
        protein_frames = reader.readlines()
    with open(endtoend_vectors_file) as reader:
        endtoend_vectors = reader.readlines()
    with open(avg_steps_file) as reader:
        avg_steps = reader.readline().strip()
    # "Real" work

    # Cleanup
    snapshot_reader.close()
    db_conn.commit()
    db_conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simsetup", type=str, help="ChroMoCa simulation input file.")
    parser.add_argument("--snapshots", type=str, help="ChroMoCa snapshots file.")
    parser.add_argument("--proteins", type=str, help="ChroMoCa parsed protein global frames file.")
    parser.add_argument("--endtoend", type=str, help="End to end distances (as defined within ChroMoCa) file.")
    parser.add_argument("--log", type=str, help="ChroMoCa run log file.")
