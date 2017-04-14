"""
    Stefjord Todolli
    April 11, 2017
"""

def write_slurm_submission_file(sbatch_file_name, job_name, walltime, memory, run_command_lines, processors=1,
                                partition="main", **kwargs):
    """Create a Slurm job submission file based on resource requirements and the set of commands that need to be run.

    :param sbatch_file_name:
    :param job_name:
    :param walltime:
    :param memory:
    :param run_command_lines:
    :param processors:
    :param partition:
    :return:
    """
    writer = open(sbatch_file_name, "w")
    writer.write("#!/bin/bash\n\n")
    writer.write("#SBATCH --partition=" + partition + "\n")
    writer.write("#SBATCH --job-name=" + job_name + "\n")
    writer.write("#SBATCH --nodes=1" + "\n")
    writer.write("#SBATCH --ntasks=" + str(processors) + "\n")
    writer.write("#SBATCH --cpus-per-task=1" + "\n")
    writer.write("#SBATCH --mem=" + str(memory) + "\n")
    writer.write("#SBATCH --time=" + walltime + "\n")
    writer.write("#SBATCH --output=slurm.%N.%j.out\n")
    writer.write("#SBATCH --export=ALL\n")
    if kwargs is not None:
        for key, arg in kwargs.items():
            writer.write("#SBATCH --{0:s}={1:s}\n".format(key, arg))
    writer.write("\n")
    writer.write(run_command_lines)
    writer.close()


def read_slurm_submission_file(sbatch_file_name):
    """Read the Slurm scheduler parameters and run commands from a Slurm job submission file.

    :param sbatch_file_name:
    :return:
    """
    reader = open(sbatch_file_name)
    sbatch_lines = reader.readlines()
    reader.close()
    slurm_parameters = {}
    for line in [l for l in sbatch_lines if "SBATCH" in l]:
        splitline = line.strip("--").split("=")
        slurm_parameters[splitline[0]] = splitline[1]
    run_command_lines = [l for l in sbatch_lines if ("#" not in l and len(l) > 1)]
    return (slurm_parameters, run_command_lines)
