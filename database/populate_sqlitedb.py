"""
    Stefjord Todolli
    Sept 15, 2017
"""

import argparse
import sqlite3 as sq
import numpy as np
import pandas as pd
from chromocaIO.chromoca_parser import parse_snapshot, parse_eed_file, parse_protein_frames


def tails_local_to_global_iter(protein_frame, tails_list):
    return(map(lambda x: np.dot(np.array(protein_frame[1]).T, x) + np.array(protein_frame[0]), np.array(tails_list)))


def add_simulation_to_sqlitedb(sqlite_db_file, setup_file, snapshots_file, protein_frames_file,
                               endtoend_distances_file, log_file):
    db_conn = sq.connect(sqlite_db_file)
    dbc = db_conn.cursor()

    db_conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simsetup", type=str, help="ChroMoCa simulation input file.")
    parser.add_argument("--snapshots", type=str, help="ChroMoCa snapshots file.")
    parser.add_argument("--proteins", type=str, help="ChroMoCa parsed protein global frames file.")
    parser.add_argument("--endtoend", type=str, help="End to end distances (as defined within ChroMoCa) file.")
    parser.add_argument("--log", type=str, help="ChroMoCa run log file.")
