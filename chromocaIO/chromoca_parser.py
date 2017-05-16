"""
    Stefjord Todolli
    April 11, 2017
"""

import numpy as np
import ast


def write_sim_input_file(sim_name, sim_n_steps, sim_monitoring_sampling, sim_init_config, mc_amplitude,
                         potential_preset, eed_filter=None, **kwargs):
    """Generate a ChroMoCa input file from the specified parameters.

    :type sim_name: str
    :type sim_n_steps: int
    :type sim_monitoring_sampling: int
    :type sim_init_config: str
    :type mc_amplitude: float
    :type eed_filter: float
    :type potential_preset: str
    """
    writer = open(sim_name+".txt", "w")
    writer.write("# simulation settings\n")
    writer.write("sim_name={0:s}\n".format(sim_name.split(".")[0]))
    writer.write("sim_n_steps={0:d}\n".format(sim_n_steps))
    writer.write("sim_monitoring="
                 "[Chromatin::{0:d};MonteCarlo::{1:d};Chromatin3D::{2:d}]\n".format(sim_monitoring_sampling, 100, 0))
    writer.write("\n# starting point\n")
    writer.write("sim_chromatin_init=[{0:s}]\n".format(sim_init_config))
    writer.write("\n# monte carlo settings\n")
    writer.write("mc_stepper_type=regular\n")
    filters = "Metropolis::1.;Collision::0."
    if eed_filter:
        filters += ";EndToEnd::{0:1.1f}".format(eed_filter)
    writer.write("mc_filters=[" + filters + "]\n")
    writer.write("mc_sampler_type=dna_and_proteins::0.25\n")
    writer.write("mc_sampling_amplitude={0:1.2f}\n".format(mc_amplitude))
    writer.write("\n# model parameters\n")
    writer.write("dna_model_preset=plain_B-DNA\n")
    writer.write("potential_settings_preset={0:s}\n".format(potential_preset))
    if kwargs is not None:
        writer.write("\n# other parameters\n")
        for key, arg in kwargs.items():
            writer.write("{0:s}={1:s}\n".format(key, arg))
    writer.close()


def write_sim_input_file_fromkwargs(**kwargs):
    """Generate a ChroMoCa input fule from the full list of key=value parameters.

    :param sim_name:
    :param kwargs:
    :return:
    """
    writer = open(kwargs["sim_name"]+".txt", "w")
    writer.write("# simulation settings\n")
    for key, arg in kwargs.items():
        writer.write("{0:s}={1:s}\n".format(key, arg))
    writer.close()


def read_sim_input_file(input_filename):
    """Read the list of parameters specified in a ChroMoCa input file.

    :param input_filename: name of ChroMoCa input file
    :type input_filename: str
    :return: dictionary of key=value parameters specified in the input file
    :rtype: dict
    """
    reader = open(input_filename)
    sim_lines = reader.readlines()
    reader.close()
    keyvalue_pairs = {}
    for line in [l.strip("\n") for l in sim_lines if "=" in l]:
        splitline = line.split("=")
        keyvalue_pairs[splitline[0]] = splitline[1]
    return keyvalue_pairs



def parse_eed_file(eed_file_name):
    """

    :type eed_file_name: str
    :rtype list
    """
    reader = open(eed_file_name)
    eed_lines = reader.readlines()
    reader.close()
    eed_list = []
    for line in eed_lines:
        eed_xyz = [float(n.strip()) for n in line.strip("\n").strip("{").strip("}").split(",")]
        eed_list.append(np.linalg.norm(eed_xyz))
    return eed_list


def parse_epdistance_file(protein_frames_file_name):
    """

    :param protein_frames_file_name:
    :return:
    """
    reader = open(protein_frames_file_name)
    frame_lines = reader.readlines()
    reader.close()
    epdistance_list = []
    for line in frame_lines:
        line = line.replace('{', '[').replace('}', ']')
        frames = ast.literal_eval(line)
        epdistance_list.append(np.linalg.norm(np.array(frames[0][0]) - np.array(frames[-1][0])))
    return epdistance_list


def parse_protein_frames(protein_frames_file_name):
    """

     :param protein_frames_file_name:
     :return:
     """
    reader = open(protein_frames_file_name)
    frame_lines = reader.readlines()
    reader.close()
    frames_list = []
    for line in frame_lines:
        line = line.replace('{', '[').replace('}', ']')
        frames = ast.literal_eval(line)
        frames_list.append(frames)
    return frames_list
