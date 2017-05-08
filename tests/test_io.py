"""
    Stefjord Todolli
    April 12, 2017
"""

import unittest, os
from chromocaIO.hpc_slurm import write_slurm_submission_file


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
        self.sbatch_test2_dependency = self.sbatch_heading + "#SBATCH --dependency=after:5666346\n\n" + \
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
        write_slurm_submission_file("sbatch_file_name1.sh", "sample-job-1", "12:00:00", 1000, self.sample_command, 1,
                                    "main")
        reader = open("sbatch_file_name1.sh")
        self.testcase1 = reader.readlines()
        reader.close()

        # Test 2 - setup
        writer = open("test2_dependency.sh", "w")
        writer.write(self.sbatch_test2_dependency)
        writer.close()
        reader = open("test2_dependency.sh")
        self.ref_testcase2 = reader.readlines()
        reader.close()
        write_slurm_submission_file("sbatch_file_name2.sh", "sample-job-1", "12:00:00", 1000, self.sample_command, 1,
                                    "main", dependency="after:5666346")
        reader = open("sbatch_file_name2.sh")
        self.testcase2 = reader.readlines()
        reader.close()

        # Test 3 - setup
        writer = open("test3_default.sh", "w")
        writer.write(self.sbatch_test3_simple_defaultarg)
        writer.close()
        reader = open("test3_default.sh")
        self.ref_testcase3 = reader.readlines()
        reader.close()
        write_slurm_submission_file("sbatch_file_name3.sh", "sample-job-1", "12:00:00", 1000, self.sample_command)
        reader = open("sbatch_file_name3.sh")
        self.testcase3 = reader.readlines()
        reader.close()

        # Test 4 - setup
        writer = open("test4_default_dependency.sh", "w")
        writer.write(self.sbatch_test4_dependency_defaultarg)
        writer.close()
        reader = open("test4_default_dependency.sh")
        self.ref_testcase4 = reader.readlines()
        reader.close()
        write_slurm_submission_file("sbatch_file_name4.sh", "sample-job-1", "12:00:00", 1000, self.sample_command,
                                    dependency="after:5666346")
        reader = open("sbatch_file_name4.sh")
        self.testcase4 = reader.readlines()
        reader.close()

    def test_simple_hpc_job(self):
        self.assertEqual(self.testcase1, self.ref_testcase1, "incorrect simple case with all positional arguments and "
                                                             "no **kwargs")

    def test_dependency_hpc_job(self):
        self.assertEqual(self.ref_testcase2, self.testcase2, "incorrect dependency case with all positional arguments "
                                                             "and one **kwarg for dependency option")

    def test_simple_defaultarg_hpc_job(self):
        self.assertEqual(self.ref_testcase3, self.testcase3, "incorrect simple case with 2 positional optional "
                                                             "arguments ommited and no **kwargs")

    def test_dependency_defaultarg_hpc_job(self):
        self.assertEqual(self.ref_testcase4, self.testcase4, "incorrect dependency case with 2 positional optional "
                                                             "arguments ommited and one **kwarg for dependency option")

    def tearDown(self):
        os.remove("sbatch_file_name1.sh")
        os.remove("sbatch_file_name2.sh")
        os.remove("sbatch_file_name3.sh")
        os.remove("sbatch_file_name4.sh")
        os.remove("test1_simple.sh")
        os.remove("test2_dependency.sh")
        os.remove("test3_default.sh")
        os.remove("test4_default_dependency.sh")


if __name__ == '__main__':
    unittest.main()