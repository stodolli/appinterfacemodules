"""
    Stefjord Todolli
    April 13, 2017
"""

import argparse
from utils.os_manager import OsManager
from chromocaIO.hpc_slurm import write_slurm_submission_file
from chromocaIO.chromoca_parser import write_sim_input_file, read_sim_input_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("jobtype", type=str, choices=["burn-in", "mc", "sa"],
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
    # parser.add_argument("--directory", type=str, default=".",
    #                     help="Directory that contains ChroMoCa input files. (defaults to current directory)")
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
    command_footer = "cp -r {0:s}/* {1:s}/\ncd ..\nrm -r {0:s}\n".format(jobdir, origindir)\
                     + "mv slurm*.${SLURM_JOBID}.out " + origindir + "/"

    input_files = osm.get_filenames_match(args.keyword)
    submit_commands = []

    # Case 1 - initial burn-in run. All ChroMoCa input files are present.
    if args.jobtype == "burn-in" and args.followup is None:
        print("Initial burn-in runs. Complete ChroMoCa input files expected.")
        for file in input_files:
            filename = file.split(".")[0]
            if osm.exists(filename):
                print("Directory '" + filename + "', already exists! Skipping input file to avoid overwriting existing "
                                                "simulation data ...")
                continue
            run_command = "{0:s}" \
                          "cp {1:s}/{2:s}.txt .\n" \
                          "{3:s} {2:s}.txt >> {2:s}.log\n" \
                          "tail -n1 {2:s}/{2:s}_snapshots.txt > {2:s}/{2:s}_last-snapshot.txt\n" \
                          "{4:s}".format(command_header, origindir, filename, chromoca, command_footer)
            write_slurm_submission_file(filename+".sh", filename, args.runtime, args.memory, run_command,
                                        args.processors)
            submit_commands.append("sbatch " + filename + ".sh")

    # Case 2 - follow up to burn-in run. Based on the followup argument number, the starting configuration will be
    # changed accordingly.
    elif args.jobtype == "burn-in" and args.followup is not None:
        print("Follow-up round " + str(args.followup) + " of burn-in runs. Previous burn-in run expected.")
        
    # Case 3 - Monte Carlo run. Depending on followup argument number, could be based on a thermalized burn-in run, or
    # could be a continuation (followup) of a previous MC run.
    elif args.jobtype == "mc":
        print("MC runs. Round " + str(args.followup) + "!")
        for file in input_files:
            filename = file.split(".")[0]

    # Case 4 - Simulated Annealing run
    elif args.jobtype == "sa":
        print("Simulated annealing run not implemented yet!")
        quit()

    # Finish up by printing all the queuing scripts that were created
    if len(submit_commands) > 0:
        print("\nTo submit all Slurm submission files created above, type:\n")
        for cmd in submit_commands:
            print(cmd)