import argparse
import ast
import re
import sqlite3 as sq
import numpy as np
import pandas as pd



def parse_snapshot(snapshot):
    parsed_snapshot = snapshot.split("|")
    [energy_term, nsteps_term, dnasteps_term, nproteins_term] = parsed_snapshot[:4]
    proteins_terms = parsed_snapshot[4:]
    energy = float(energy_term.split("::")[1])
    nsteps = int(nsteps_term.split("::")[1])
    dnasteps = ast.literal_eval(dnasteps_term.split("::")[1].replace("{", "[").replace("}", "]").replace(";", ","))
    nproteins = int(nproteins_term.split("::")[1])
    protein_names = [p.split("#")[0].split("[")[1] for p in proteins_terms]
    protein_indices = [int(p.split("@")[1]) for p in proteins_terms]
    local_tails = [ast.literal_eval(re.sub(r".*#|].*", "", p).replace("{", "[").replace("}", "]").replace("_", ","))
                   for p in proteins_terms]
    return(energy, nsteps, dnasteps, nproteins, protein_names, protein_indices, local_tails)


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
