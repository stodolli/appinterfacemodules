"""
    Stefjord Todolli
    April 13, 2017
"""

import argparse
from utils.os_manager import OsManager
from chromocaIO.hpc_slurm import write_slurm_submission_file
from chromocaIO.chromoca_parser import write_sim_input_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job-type", dest="jobtype", nargs=1, type=str, choices=["burn-in", "initial-mc", "followup-mc"],
                        help="Specify simulation type set up in the input file.")
    parser.add_argument("keyword", nargs=1, type=str,
                        help="Keyword to match ChroMoCa input files that will be run in the cluster.")
    args = parser.parse_args()

    osm = OsManager()

    if args.jobtype == "burn-in":
        pass
    elif args.jobtype == "initial-mc":
        pass
    elif args.jobtype == "followup-mc":
        pass
    else:
        quit()