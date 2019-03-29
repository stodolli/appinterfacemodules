"""
    Stefjord Todolli
    April 13, 2017
"""
import os, sys
fullprojectpath = os.path.realpath(__file__).rsplit("/", 2)[0]
if fullprojectpath not in sys.path:
    sys.path.extend([fullprojectpath])


import argparse
import numpy as np
from utils.os_manager import OsManager
from chromocaIO.hpc_slurm import write_slurm_submission_file, read_slurm_submission_file
from chromocaIO.chromoca_parser import write_sim_input_file_fromkwargs, read_sim_input_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("jobtype", type=str, choices=["burn-in", "mc", "epc", "sa"],
                        help="Specify simulation type intended in the input file.")
    parser.add_argument("keyword", type=str,
                        help="Keyword to match ChroMoCa input files that will be run in the cluster.")
    parser.add_argument("--followup", type=int, help="Follow up simulation based on data from a previous run."
                                                     "1 for coming from burn-in run, 2+ for consequent runs.")
    parser.add_argument("-t", "--runtime", type=str, default="12:00:00",
                        help="Compute time (d-HH:MM:SS) requirement for Slurm. (default 05:00:00)")
    parser.add_argument("-m", "--memory", type=int, default=1000,
                        help="Memory (in MB) requirement for Slurm. (default 1000)")
    parser.add_argument("-p", "--processors", type=int, default=1,
                        help="Number of processors requirement for Slurm. (default 1)")
    parser.add_argument("--partition", type=str, default="main",
                        help="Partition in which to queue the job.")
    parser.add_argument("--sim_n_steps", type=int, help="Number of MC steps for the new simulation.")
    parser.add_argument("--epc_constraint", type=float, help="End-to-end distance constraint for epc simulation.")
    parser.add_argument("--annealing", type=str, help="Parameters for simulated annealing simulation. "
                                                      "(T0+schedule+reduction_factor")
    parser.add_argument("--file_numbering_format", type=int, default=2,
                        help="Number of digits to place for numbering of simulation files (i.e., mc1 or mc01).")
    parser.add_argument("--scratchdir", type=str, default="/scratch/st468",
                        help="Scratch directory for cluster user. (default is /scratch/st468)")
    parser.add_argument("--executable", type=str, default="/home/st468/local_installs/chromatin/bin/chromoca",
                        help="Full path to ChroMoCa executable. "
                             "(default is /home/st468/local_installs/chromatin/bin/chromoca)")
    args = parser.parse_args()

    osm = OsManager()
    origindir = osm.curr_dir()
    jobdir = args.scratchdir + "/${SLURM_JOBID}"
    chromoca = args.executable
    command_header = "\nmkdir {0:s}\ncd {0:s}\n".format(jobdir)
    command_footer = "\nrm {0:s}/*_last-snapshot.txt\ncp -r {0:s}/* {1:s}/\n" \
                     "cd ..\nrm -r {0:s}\n".format(jobdir, origindir)
    input_files = [f for f in osm.get_filenames_match(args.keyword) if ".txt" in f]
    submit_commands = []
    file_num_formatter = "{0:0" + str(args.file_numbering_format) + "d}"

    # Case 1 - initial burn-in run. All ChroMoCa input files are present.
    if args.jobtype == "burn-in" and args.followup is None:
        command_footer = "\ncp -r {0:s}/* {1:s}/\ncd ..\nrm -r {0:s}\n".format(jobdir, origindir)
        print("Initial burn-in runs. Complete ChroMoCa input files expected.")
        for file in input_files:
            filename = file.split(".")[0]
            if osm.exists(filename):
                print("Directory '" + filename + "' already exists! Skipping input file to avoid overwriting existing "
                                                "simulation data ...")
                continue
            elif osm.exists(filename + ".sh"):
                print("File '" + filename + ".sh' already exists! Skipping input file to avoid overwriting data.")
                continue
            run_command = "{0:s}\n" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "{3:s} {2:s}.txt >> {2:s}.log\n" \
                          "tail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{4:s}".format(command_header, origindir, filename, chromoca, command_footer)
            write_slurm_submission_file(filename+".sh", filename, args.runtime, args.memory, run_command,
                                        args.processors, args.partition)
            submit_commands.append("sbatch " + filename + ".sh")

    # Case 2 - follow up to burn-in run. Based on the followup argument number, the starting configuration will be
    # changed accordingly. If this is another burn-in run, MC step needs to be MANUALLY adjusted afterwards!
    elif args.jobtype == "burn-in" and args.followup is not None:
        print("Follow-up, round " + str(args.followup) + " of burn-in runs. Previous burn-in run expected.")
        print("If this is another burn-in run to tune acceptance rate, MC step needs to be MANUALLY adjusted!")
        for file in input_files:
            existing_filename = file.split(".")[0]
            new_filename = existing_filename.split("--")[0] + "--burn" + str(args.followup)
            if osm.exists(new_filename):
                print("Directory '" + new_filename + "', already exists! Skipping input file to avoid overwriting "
                                                     "existing simulation data ...")
                continue
            elif osm.exists(new_filename + ".txt"):
                print("File '" + new_filename + ".txt' already exists! Skipping input file to avoid overwriting data.")
                continue
            # starting_config = "{0:s}/{1:s}/{1:s}_last-snapshot.txt".format(origindir, existing_filename)
            starting_config = "{0:s}_last-snapshot.txt".format(existing_filename)
            chromoca_params = read_sim_input_file(file)
            chromoca_params["sim_name"] = new_filename
            chromoca_params["sim_chromatin_init"] = "[snapshot::{0:s}]".format(starting_config)
            if args.sim_n_steps is not None:
                chromoca_params["sim_n_steps"] = "{0:d}".format(args.sim_n_steps)
            write_sim_input_file_fromkwargs(**chromoca_params)
            (slurm_params, slurm_run_commands) = read_slurm_submission_file(existing_filename + ".sh")
            slurm_runtime = slurm_params["time"]
            slurm_memory = slurm_params["mem"]
            slurm_procs = slurm_params["ntasks"]
            run_command = "{0:s}" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "cp {1:s}/{3:s}/{3:s}_last-snapshot.txt .\n" \
                          "\n{4:s} {2:s}.txt >> {2:s}.log\n" \
                          "tail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{5:s}".format(command_header, origindir, new_filename, existing_filename, chromoca,
                                         command_footer)
            write_slurm_submission_file(new_filename+".sh", new_filename, slurm_runtime, slurm_memory, run_command,
                                        slurm_procs, args.partition)
            submit_commands.append("sbatch " + new_filename + ".sh")

    # Case 3 - Monte Carlo run. Similar to initial burn-in runs, is based on an existing input file. Mainly used for
    # initial step of a conditional sampling run for now.
    elif args.jobtype == "mc" and args.followup is None:
        print("MC run. Round 1!")
        command_footer = "\ncp -r {0:s}/* {1:s}/\ncd ..\nrm -r {0:s}\n".format(jobdir, origindir)
        for file in input_files:
            filename = file.split(".")[0]
            if osm.exists(filename):
                print("Directory '" + filename + "' already exists! Skipping input file to avoid overwriting existing "
                                                "simulation data ...")
                continue
            elif osm.exists(filename + ".sh"):
                print("File '" + filename + ".sh' already exists! Skipping input file to avoid overwriting data.")
                continue
            command_post_process = "{0:s}_parser --rebuild-protein-frames " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_proteins.txt\n" \
                                   "{0:s}_parser --rebuild-end-to-end " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_endtoend.txt\n".format(chromoca, filename)
            chromoca_params = read_sim_input_file(file)
            init_config = chromoca_params["sim_chromatin_init"].split("::")[1].rstrip("]")
            run_command = "{0:s}\n" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "cp {1:s}/{3:s} .\n" \
                          "\n{4:s} {2:s}.txt >> {2:s}.log\n" \
                          "\ntail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{5:s}{6:s}".format(command_header, origindir, filename, init_config, chromoca,
                                              command_post_process, command_footer)
            write_slurm_submission_file(filename+".sh", filename, args.runtime, args.memory, run_command,
                                        args.processors, args.partition)
            submit_commands.append("sbatch " + filename + ".sh")


    # Case 4 - Monte Carlo run. Depending on followup argument number, could be based on a thermalized burn-in run, or
    # could be a continuation (followup) of a previous MC run.
    elif args.jobtype == "mc" and args.followup is not None:
        print("MC runs. Round " + str(args.followup) + "!")
        for file in input_files:
            existing_filename = file.split(".")[0]
            # TODO: conditional statement code not covered - unused
            if args.followup is None:
                if "burn" in existing_filename:
                    followup = 1
                else:
                    followup = int(existing_filename.split("--")[1].lstrip("mc")) + 1
            else:
                followup = args.followup
            new_filename = existing_filename.split("--")[0] + "--mc" + file_num_formatter.format(followup)
            if osm.exists(new_filename):
                print("Directory '" + new_filename + "', already exists! Skipping input file to avoid overwriting "
                                                     "existing simulation data ...")
                continue
            elif osm.exists(new_filename + ".txt"):
                print("File '" + new_filename + ".txt' already exists! Skipping input file to avoid overwriting data.")
                continue
            starting_config = "{0:s}_last-snapshot.txt".format(existing_filename)
            chromoca_params = read_sim_input_file(file)
            chromoca_params["sim_name"] = new_filename
            chromoca_params["sim_chromatin_init"] = "[snapshot::{0:s}]".format(starting_config)
            if args.sim_n_steps is not None:
                chromoca_params["sim_n_steps"] = "{0:d}".format(args.sim_n_steps)
            write_sim_input_file_fromkwargs(**chromoca_params)
            command_post_process = "{0:s}_parser --rebuild-protein-frames " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_proteins.txt\n" \
                                   "{0:s}_parser --rebuild-end-to-end " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_endtoend.txt\n".format(chromoca,
                                                                                                   new_filename)
            run_command = "{0:s}" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "cp {1:s}/{3:s}/{3:s}_last-snapshot.txt .\n" \
                          "\n{4:s} {2:s}.txt >> {2:s}.log\n" \
                          "\ntail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{5:s}{6:s}".format(command_header, origindir, new_filename, existing_filename, chromoca,
                                              command_post_process, command_footer)
            write_slurm_submission_file(new_filename + ".sh", new_filename, args.runtime, args.memory, run_command,
                                        args.processors, args.partition)
            submit_commands.append("sbatch " + new_filename + ".sh")

    # Case 5 - EPC constrained MC run.
    # TODO all these methods need to be cleaned up!
    elif args.jobtype == "epc" and args.followup is None and args.epc_constraint is not None:
        followup = 1
        print("EPC runs with distance constraint \nRound " + str(followup) + "!")
        for file in input_files:
            chromoca_params = read_sim_input_file(file)
            existing_filename = file.split(".")[0]
            new_filename = existing_filename.split("--")[0] + "-epc{0:.0f}".format(args.epc_constraint) + "--mc" + \
                           file_num_formatter.format(followup)
            if osm.exists(new_filename):
                print("Directory '" + new_filename + "', already exists! Skipping input file to avoid overwriting "
                                                     "existing simulation data ...")
                continue
            elif osm.exists(new_filename + ".txt"):
                print("File '" + new_filename + ".txt' already exists! Skipping input file to avoid overwriting data.")
                continue
            starting_config = "{0:s}--shortEP-snapshot.txt".format(existing_filename.split("--")[0])
            chromoca_params["sim_name"] = new_filename
            chromoca_params["sim_chromatin_init"] = "[snapshot::{0:s}]".format(starting_config)
            if args.sim_n_steps is not None:
                chromoca_params["sim_n_steps"] = "{0:d}".format(args.sim_n_steps)
            mc_filters = chromoca_params["mc_filters"].strip("[").strip("]").split(";")
            mc_filters.append("EndToEnd::{0:1.1f}".format(args.epc_constraint))
            new_mc_filters = "[" + mc_filters[0]
            for filter in mc_filters[1:]:
                new_mc_filters += ";" + filter
            new_mc_filters += "]"
            chromoca_params["mc_filters"] = new_mc_filters
            write_sim_input_file_fromkwargs(**chromoca_params)
            command_post_process = "{0:s}_parser --rebuild-protein-frames " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_proteins.txt\n" \
                                   "{0:s}_parser --rebuild-end-to-end " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_endtoend.txt\n".format(chromoca,
                                                                                                   new_filename)
            run_command = "{0:s}" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "cp {1:s}/{3:s}--shortEP-snapshot.txt .\n" \
                          "\n{4:s} {2:s}.txt >> {2:s}.log\n" \
                          "\ntail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{5:s}{6:s}".format(command_header, origindir, new_filename, existing_filename.split("--")[0],
                                              chromoca, command_post_process, command_footer)
            write_slurm_submission_file(new_filename + ".sh", new_filename, args.runtime, args.memory, run_command,
                                        args.processors, args.partition)
            submit_commands.append("sbatch " + new_filename + ".sh")

    # Case 6 - Simulated Annealing run. Normally is run as a followup to a MC run, burn-in run, or another simulated
    # annealing run.
    elif args.jobtype == "sa" and args.followup is not None:
        print("SA runs. Round " + str(args.followup) + "!")
        for file in input_files:
            existing_filename = file.split(".")[0]
            followup = args.followup
            new_filename = existing_filename.split("--")[0] + "--sa" + file_num_formatter.format(followup)
            if osm.exists(new_filename):
                print("Directory '" + new_filename + "', already exists! Skipping input file to avoid overwriting "
                                                     "existing simulation data ...")
                continue
            elif osm.exists(new_filename + ".txt"):
                print("File '" + new_filename + ".txt' already exists! Skipping input file to avoid overwriting data.")
                continue
            starting_config = "{0:s}_last-snapshot.txt".format(existing_filename)
            chromoca_params = read_sim_input_file(file)
            chromoca_params["sim_name"] = new_filename
            chromoca_params["sim_chromatin_init"] = "[snapshot::{0:s}]".format(starting_config)
            if args.sim_n_steps is not None:
                chromoca_params["sim_n_steps"] = "{0:d}".format(args.sim_n_steps)
                sim_n_steps = args.sim_n_steps
            else:
                sim_n_steps = int(chromoca_params["sim_n_steps"])
            if args.followup == 1 or args.annealing is not None:
                annealing_params = [float(param) for param in args.annealing.split("+")]
            else:
                [t0, schedule, factor] = [float(param) for param in
                                          chromoca_params["mc_stepper_type"].split("::")[1].split("+")]
                t1 = t0 * np.power(factor, sim_n_steps/schedule)
                annealing_params = [t1, schedule, factor]
            chromoca_params["mc_stepper_type"] = "annealing::{0:1.4f}+{1:1.0f}+{2:1.2f}".format(*annealing_params)
            write_sim_input_file_fromkwargs(**chromoca_params)
            command_post_process = "{0:s}_parser --rebuild-protein-frames " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_proteins.txt\n" \
                                   "{0:s}_parser --rebuild-end-to-end " \
                                   "{1:s}/{1:s}_snapshots.txt > {1:s}/{1:s}_endtoend.txt\n".format(chromoca,
                                                                                                   new_filename)
            run_command = "{0:s}" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "cp {1:s}/{3:s}/{3:s}_last-snapshot.txt .\n" \
                          "\n{4:s} {2:s}.txt >> {2:s}.log\n" \
                          "\ntail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{5:s}{6:s}".format(command_header, origindir, new_filename, existing_filename, chromoca,
                                              command_post_process, command_footer)
            write_slurm_submission_file(new_filename + ".sh", new_filename, args.runtime, args.memory, run_command,
                                        args.processors, args.partition)
            submit_commands.append("sbatch " + new_filename + ".sh")


    # Finish up by printing all the queuing scripts that were created
    if len(submit_commands) > 0:
        print("\nTo submit all Slurm submission files created above, type:\n")
        for cmd in submit_commands:
            print(cmd)