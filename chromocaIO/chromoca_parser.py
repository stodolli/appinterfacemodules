"""
    Stefjord Todolli
    April 11, 2017
"""

import numpy as np


def write_sim_input_file(sim_name, sim_n_steps, sim_monitoring_sampling, sim_init_config, mc_amplitude,
                         potential_preset, eed_filter, **kwargs):
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
    writer.write("# simulation settings")
    writer.write("sim_name=" + sim_name)
    writer.write("sim_n_steps=" + str(sim_n_steps))
    writer.write("sim_monitoring=[Chromatin::" + str(sim_monitoring_sampling) + ";MonteCarlo::" + str(100) +
                 ";Chromatin3D::" + str(0) + "]")
    writer.write("\n# starting point")
    writer.write("sim_chromatin_init=[" + sim_init_config + "]")
    writer.write("\n monte carlo settings")
    writer.write("mc_stepper=regular")
    filters = "Metropolis::1.;Collision::0."
    if eed_filter:
        filters += ";EndToEnd::{0:s}".format(eed_filter)
    writer.write("mc_filters=[" + filters + "]")
    writer.write("mc_sampler_type=dna_and_proteins::0.25")
    writer.write("mc_sampling_amplitude=" + mc_amplitude)
    writer.write("\n# model parameters")
    writer.write("dna_model_preset=plain_B-DNA")
    writer.write("potential_settings_preset=" + potential_preset)
    writer.write("\n# other parameters")
    for key, arg in kwargs.items():
        writer.write("{0:s}={1:s}".format(key, arg))
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
    keyvalue_pairs = {}
    for line in [l for l in sim_lines if "=" in l]:
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
