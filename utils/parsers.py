"""
    Stefjord Todolli
    May 10, 2017
"""

import numpy as np


class BPparser:
    '''A class that contains parsers to read bp parameter and reference frame files.'''

    @staticmethod
    def read_bp_frames(ref_frames_file, normalize=False):
        ref_frames = []
        ref_file = open(ref_frames_file, "r")
        ref_lines = ref_file.readlines()
        for _i in range(int(ref_lines[0].split()[0])):
            description = ref_lines[_i * 5 + 1].strip()
            origin = [float(f) for f in ref_lines[_i * 5 + 2].split()[:3]]
            x = [float(f) for f in ref_lines[_i * 5 + 3].split()[:3]]
            y = [float(f) for f in ref_lines[_i * 5 + 4].split()[:3]]
            z = [float(f) for f in ref_lines[_i * 5 + 5].split()[:3]]
            if normalize:
                x = (x / np.linalg.norm(x)).tolist()
                y = (y / np.linalg.norm(y)).tolist()
                z = (z / np.linalg.norm(z)).tolist()
            ref_frames.append([description, origin, [x, y, z]])
        ref_file.close()
        return ref_frames

    @staticmethod
    def write_bp_frames(ref_frames, ref_frames_file, precision=4):
        printer = open(ref_frames_file, 'w')
        printer.write("{0:5d} base pairs\n".format(len(ref_frames)))
        frames_formatter = "{0:10." + str(precision) + "f} {1:10." + str(precision) + "f} {2:10." + str(
            precision) + "f} "
        for frame in ref_frames:
            printer.write(frame[0] + "\n")
            printer.write(frames_formatter.format(*frame[1]) + " # origin\n")
            printer.write(frames_formatter.format(*frame[2][0]) + " # x-axis\n")
            printer.write(frames_formatter.format(*frame[2][1]) + " # y-axis\n")
            printer.write(frames_formatter.format(*frame[2][2]) + " # z-axis\n")
        printer.close()

    @staticmethod
    def read_bp_parameters(bp_params_file):
        bp_params = []
        par_file = open(bp_params_file, "r")
        par_lines = par_file.readlines()
        # Shear, Stretch, Stagger, Buckle, Prop-Tw, Opening, Shift, Slide, Rise, Tilt, Roll, Twist
        assert int(par_lines[0].split()[0]) == len(par_lines[3:])
        for line in par_lines[3:]:
            if len(line) > 0:
                pars = line.split()
                bp_params.append([pars[0]] + [float(f) for f in pars[1:]])
        par_file.close()
        return bp_params

    @staticmethod
    def write_bp_parameters(bp_parameters, bp_params_file):
        printer = open(bp_params_file, "w")
        printer.write(" {0:1d} # base-pairs\n".format(len(bp_parameters)))
        printer.write("   0 # ***local base-pair & step parameters***\n")
        printer.write("#        Shear   Stretch    Stagger   Buckle   Prop-Tw   Opening     " +
                      "Shift     Slide      Rise      Tilt      Roll     Twist")
        formatter = "{{{0:1d}:4s}}".format(0)
        for i in range(1, 13):
            formatter += "{{{0:1d}:10.5f}}".format(i)
        for bp_par in bp_parameters:
            printer.write("\n" + formatter.format(*bp_par))
        printer.close()
