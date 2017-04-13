"""
    Stefjord Todolli
    April 13, 2017
"""

import os, shutil


class OsManager:
    def curr_dir(self):
        return os.getcwd()

    def change_dir(self, directory):
        os.chdir(directory)

    def exists(self, path):
        return os.path.exists(path)

    def make_dir(self, directory):
        os.mkdir(directory, mode=755)

    def get_filenames(self, directory="."):
        files = [f for f in os.listdir(directory) if not os.path.isdir(os.path.join(directory, f))]
        files.sort()
        return files

    def get_filenames_match(self, expression, directory="."):
        allfiles = [f for f in os.listdir(directory) if not os.path.isdir(os.path.join(directory, f))]
        files = [f for f in allfiles if expression in f]
        files.sort()
        return files

    def get_directorynames(self, directory="."):
        directories = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        directories.sort()
        return directories

    def get_directorynames_match(self, expression, directory="."):
        alldirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        dirs = [d for d in alldirs if expression in d]
        dirs.sort()
        return dirs

    def copy_file(self, filename, destination):
        shutil.copy2(filename, destination)

    def copy_directory(self, directory, destination):
        shutil.copytree(directory, destination)

    def rename(self, old_name, new_name):
        os.rename(old_name, new_name)

    def delete_file(self, filename):
        os.remove(filename)

    def delete_files(self, filenames):
        for f in filenames:
            os.remove(f)

    def delete_files_except(self, directory, exclude):
        filenames = [f for f in os.listdir(directory)
                     if not os.path.isdir(os.path.join(directory, f)) and f not in exclude]
        for _f in filenames:
            os.remove(_f)
