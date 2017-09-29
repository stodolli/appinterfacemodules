"""
    Stefjord Todolli
    Sept 15, 2017
"""

import argparse
import sqlite3 as sq
import numpy as np
from chromocaIO.chromoca_parser import parse_snapshot, parse_eed_file, parse_protein_frames, read_sim_input_file
from utils.structure_properties import radius_gyration, sedimentation_coefficient


def tails_local_to_global_iter(protein_frame, tails_list):
    return(map(lambda x: np.dot(np.array(protein_frame[1]).T, x) + np.array(protein_frame[0]), np.array(tails_list)))


def add_simulation_to_sqlitedb(sqlite_db_file, sim_type, sim_description, snapshots_file, sim_setup_file,
                               starting_config_file, log_file, protein_frames_file, endtoend_vectors_file,
                               avg_steps_file, mc_temp=1.0):
    ### Open files
    snapshot_reader = open(snapshots_file)
    sim_setup = read_sim_input_file(sim_setup_file)
    with open(sim_setup_file) as reader:
        simulation_input = reader.readlines()
    with open(starting_config_file) as reader:
        starting_config = reader.readline().strip()
    with open(log_file) as reader:
        sim_log = reader.readlines()
    with open(protein_frames_file) as reader:
        protein_frames = list(parse_protein_frames(reader.readlines())) #TODO: needs to be done using mapping
    with open(endtoend_vectors_file) as reader:
        endtoend_vectors = list(parse_eed_file(reader.readlines()))     #TODO: needs to be done using mapping
    with open(avg_steps_file) as reader:
        avg_steps = reader.readline().strip()
    #################################################################
    ##### Setup
    #################################################################
    db_conn = sq.connect(sqlite_db_file)
    dbc = db_conn.cursor()
    parsed_starting_config = parse_snapshot(starting_config)
    n_dnasteps = parsed_starting_config[1]
    dnabp_num = n_dnasteps + 1
    n_proteins = parsed_starting_config[3]
    [protein_names, protein_indices] = parsed_starting_config[4:5]
    start_date = [l.split("=")[1] for l in sim_log if "start date" in l][0].strip()
    end_date = [l.split("=")[1] for l in sim_log if "end date" in l][-1].strip()
    protein_models_options = dbc.execute('SELECT protein_model_name, protein_model_id, binding_domain_start, '
                                         'binding_domain_end FROM protein_models')
    protein_models_map = {}
    for p in protein_models_options:
        protein_models_map[p[0]] = p[1:]
    end_range = [protein_indices[i] + protein_models_map[protein_names[i]][1]
                 for i in range(len(protein_indices))] + [dnabp_num]
    start_range = [0] + [protein_indices[i] + protein_models_map[protein_names[i]][2]
                         for i in range(len(protein_indices))]
    unbound_dnasteps = [(start, end) for (start, end) in zip(start_range, end_range) if (end - start) > 1]
    protein_details = [dbc.execute('SELECT protein_model_id, mobile_tail_charge, mobile_tail_map '
                                   'FROM protein_models WHERE protein_model_name=?', (p,)).fetchone()
                       for p in protein_names]
    ep_proteins_bool = "RNAP" in protein_names
    #################################################################
    ##### "Real" work
    #################################################################
    # INSERT INTO simulations
    dbc.execute('INSERT INTO simulations (simulation_description, simulation_part, '
                'nrl, dnasteps_num, proteins_num, unbound_dnalinkers_num, ep_proteins, '
                'mc_simulation_type, mc_sampler_type, mc_protein_sampling_frequency, '
                'mc_sampling_amplitude, mc_temperature, dna_model_preset, potential_model_preset, '
                'start_date, end_date, simulation_input, starting_config, average_steps, '
                'simulation_log) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (#sim_setup['sim_name'].rstrip("".join([str(x) for x in range(0, 10)])),
                 sim_description,
                 int(sim_setup['sim_name'].split("--")[-1][2:]),
                 int(sim_setup['sim_name'].split("x")[0]),
                 n_dnasteps, n_proteins, len(unbound_dnasteps),
                 ep_proteins_bool,
                 sim_type,
                 sim_setup['mc_sampler_type'].split("::")[0],
                 float(sim_setup['mc_sampler_type'].split("::")[1]),
                 sim_setup['mc_sampling_amplitude'],
                 mc_temp,
                 sim_setup['dna_model_preset'],
                 sim_setup['potential_settings_preset'],
                 start_date, end_date,
                 "".join(simulation_input),
                 starting_config, avg_steps,
                 "".join(sim_log)
                )
                )
    simulation_id = dbc.lastrowid
    for i in range(len(endtoend_vectors)):
        (energy, nsteps, dnasteps, nproteins,
         protein_names, protein_indices, local_tails) = parse_snapshot(snapshot_reader.readline())
        if ep_proteins_bool:
            ep_dist = np.linalg.norm(np.array(protein_frames[i][0][0]) - np.array(protein_frames[i][-1][0]))
            sc = sedimentation_coefficient(protein_frames[i][1:-1])
        else:
            ep_dist = None
            sedimentation_coefficient(protein_frames)
        # INSERT INTO structures
        dbc.execute('INSERT INTO structures (simulation_id, energy, endtoend_x, endtoend_y, endtoend_z, endtoend_dist, '
                    'ep_distance, radius_gyration, sedimentation_coeff) VALUES (?,?,?,?,?,?,?,?,?)',
                    (simulation_id, energy, endtoend_vectors[i][0], endtoend_vectors[i][1], endtoend_vectors[i][2],
                     np.linalg.norm(endtoend_vectors[i]),
                     ep_dist, radius_gyration(protein_names[i]), sc))
        structure_id = dbc.lastrowid
        protein_id_list = []
        for p in range(len(protein_names)):
            [o, [x, y, z]] = protein_frames[i][p]
            (pmodel_id, mobile_charge, tail_map) = protein_details[p]
            # INSERT INTO proteins
            dbc.execute('INSERT INTO proteins VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        (pmodel_id, structure_id, p+1,
                         o[0], o[1], o[2],
                         x[0], x[1], x[2],
                         y[0], y[1], y[2],
                         z[0], z[1], z[2]))
            protein_id_list.append(dbc.lastrowid)
            if mobile_charge is not None:
                global_tails = tails_local_to_global_iter(protein_frames[i][p], local_tails[p])
                t = 0
                for (lt, gt) in zip(local_tails[p], global_tails):
                    # INSERT INTO histone_tails
                    dbc.execute('INSERT INTO histone_tails VALUES (NULL,?,?,?,?,?,?,?,?,?)',
                                (dbc.lastrowid, tail_map[t], mobile_charge,
                                 lt[0], lt[1], lt[2],
                                 gt[0], gt[1], gt[2]))
                    t += 1
        for p1 in range(len(protein_id_list) - 1):
            for p2 in range(p1 + 1, len(protein_id_list)):
                distance = np.linalg.norm(np.array(protein_frames[i][p1][0]) - np.array(protein_frames[i][p2][0]))
                # INSERT INTO protein_interactions
                dbc.execute('INSERT INTO protein_interactions VALUES (NULL,?,?,?,NULL,NULL,NULL)',
                            (protein_id_list[p1], protein_id_list[p2], distance))

    #################################################################
    ### Cleanup
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
