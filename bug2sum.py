#!/usr/bin/env python

import os
import shutil
import argparse
import tempfile
from distutils import dir_util
from argparse import ArgumentDefaultsHelpFormatter


class Bug2SumGenerator(object):

    _SUMMARY_DIR = os.path.join('.', 'summary')
    _TIMEUNIT_EXT = '.timeunit'
    _TIME_EXT = '.time'

    def __init__(self, root_folder):
        if Bug2SumGenerator.check_root_folder(root_folder):
            self.root_folder = root_folder
            self.tmp_dir = tempfile.mkdtemp()
        else:
            print('Cannot found the Bug_ID and timeunit from {} folder.'.format(root_folder))
            exit(-1)

    @staticmethod
    def _touch(filename, time=None):
        if not os.path.exists(filename):
            try:
                with open(filename, 'a'):
                    os.utime(filename, time)
            except:
                print('[ERROR] cannot create {} file.'.format(filename))

    @staticmethod
    def _get_dir_basename(path):
        return [x for x in path.split(os.sep) if x][-1]

    @staticmethod
    def check_root_folder(root_folder):
        if '.' in Bug2SumGenerator._get_dir_basename(root_folder):
            return True
        return False

    def generate_summary_content(self, bug_tmp_dir, timeunit):
        timeunit_name = timeunit + Bug2SumGenerator._TIMEUNIT_EXT
        for root, dirs, files in os.walk(bug_tmp_dir):
            if not dirs:
                timeunit_path = os.path.join(root, timeunit_name)
                if not os.path.exists(timeunit_path):
                    os.makedirs(timeunit_path)
                for f in files:
                    time_fname = f.split('.')[0] + Bug2SumGenerator._TIME_EXT
                    time_path = os.path.join(timeunit_path, time_fname)
                    Bug2SumGenerator._touch(time_path)
            for f in files:
                os.remove(os.path.join(root, f))

    def run(self):
        bug_id, time_unit = Bug2SumGenerator._get_dir_basename(self.root_folder).split('.')
        print('[INFO] Generating BugID: {}, Timeunit {} ...'.format(bug_id, time_unit))
        bug_tmp_dir = os.path.join(self.tmp_dir, bug_id)
        shutil.copytree(self.root_folder, bug_tmp_dir)
        self.generate_summary_content(bug_tmp_dir, time_unit)

        bug_dir = os.path.join(Bug2SumGenerator._SUMMARY_DIR, bug_id)
        dir_util.copy_tree(bug_tmp_dir, bug_dir)
        print('[INFO] Generate {} with Timeunit {} done.'.format(bug_dir, time_unit))
        shutil.rmtree(bug_tmp_dir)


def main():
    arg_parser = argparse.ArgumentParser(description='Summary Generator',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-d', '--dir', dest='root_folder', action='store', default='.',
                            help='the root folder', required=True)
    args = arg_parser.parse_args()
    gen = Bug2SumGenerator(args.root_folder)
    gen.run()

if __name__ == '__main__':
    main()
