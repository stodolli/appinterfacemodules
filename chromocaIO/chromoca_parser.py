
import numpy as np


def setup_sim_input_file(sim_name, sim_n_steps, sim_monitoring_sampling, sim_init_config, eed_filter, mc_amplitude):
    """

    :type sim_name: str
    :type sim_n_steps: int
    :type sim_monitoring_sampling: int
    :type sim_init_config: str
    :type eed_filter: float
    :type mc_amplitude: float
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
    writer.write("mc_filters=[Metropolis::1.;Collision::0.;EndToEnd::" + str(eed_filter) + "]")
    writer.write("mc_sampler_type=dna_and_proteins::0.25")
    writer.write("mc_sampling_amplitude=" + mc_amplitude)
    writer.write("\n# model parameters")
    writer.write("dna_model_preset=plain_B-DNA")
    writer.write("potential_settings_preset=divalent_vasily")
    writer.close()


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

