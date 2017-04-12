"""
    Stefjord Todolli
    April 12, 2017
"""

import unittest, os
from chromocaIO.hpc_job import write_slurm_submission_file

class ChromocaIOTestCase(unittest.TestCase):

    def setUp(self):
        self.sample_command = "run command line 1\nrun command line 2\n\nrun command line 3"
        self.sbatch_heading = "#!/bin/bash\n\n" \
                            "#SBATCH --partition=main\n" \
                            "#SBATCH --job-name=sample-job-1\n" \
                            "#SBATCH --nodes=1\n" \
                            "#SBATCH --ntasks=1\n" \
                            "#SBATCH --cpus-per-task=1\n" \
                            "#SBATCH --mem=1000\n" \
                            "#SBATCH --time=12:00:00\n" \
                            "#SBATCH --output=slurm.%N.%j.out\n" \
                            "#SBATCH --export=ALL\n"
        self.sbatch_test1_simple = self.sbatch_heading + "\n" + self.sample_command
        self.sbatch_test2_dependency = self.sbatch_heading + "#SBATCH --dependency=after:5666346\n" + \
                                       self.sample_command
        self.sbatch_test3_simple_defaultarg = self.sbatch_test1_simple
        self.sbatch_test4_dependency_defaultarg = self.sbatch_test2_dependency

        # Test 1 - setup
        writer = open("test1_simple.sh", "w")
        writer.write(self.sbatch_test1_simple)
        writer.close()
        reader = open("test1_simple.sh")
        self.ref_testcase1 = reader.readlines()
        reader.close()
        write_slurm_submission_file("sbatch_file_name.sh", "sample-job-1", "12:00:00", 1000, self.sample_command, 1,
                                    "main")
        reader = open("sbatch_file_name.sh")
        self.testcase1 = reader.readlines()
        reader.close()

        # Test 2 - setup

    def test_simple_hpc_job(self):
        self.assertEqual(self.testcase1, self.ref_testcase1, "incorrect simple case with no **kwargs")

    def tearDown(self):
        os.remove("sbatch_file_name.sh")
        os.remove("test1_simple.sh")