#!/usr/bin/env python

import os
import re
import json
import shutil
import argparse
import tempfile
from distutils import dir_util
from argparse import ArgumentDefaultsHelpFormatter

from time import gmtime, strftime, mktime
import datetime


class Bug2SumGenerator(object):

    _SUMMARY_DIR = os.path.join('.', 'summary')
    _TIMEUNIT_EXT = '.timeunit'

    def __init__(self, root_folder):
        if Bug2SumGenerator.check_root_folder(root_folder):
            self.root_folder = root_folder
            self.tmp_dir = tempfile.mkdtemp()
        else:
            print('Cannot found the Bug_ID and timeunit from {} folder.'.format(root_folder))
            exit(-1)

    @staticmethod
    def _get_dir_basename(path):
        return [x for x in path.split(os.sep) if x][-1]

    @staticmethod
    def check_root_folder(root_folder):
        if '.' in Bug2SumGenerator._get_dir_basename(root_folder):
            return True
        return False

    def create_bug_folder(self, bug_id):
        bug_dir = os.path.join(self.tmp_dir, bug_id)
        if not os.path.exists(bug_dir):
            os.makedirs(bug_dir)
        return bug_dir

    def generate_summary_content(self, bug_tmp_dir, timeunit):
        timeunit_name = timeunit + Bug2SumGenerator._TIMEUNIT_EXT
        for root, dirs, files in os.walk(bug_tmp_dir):
            for f in files:
                os.remove(os.path.join(root, f))
            if not dirs:
                timeunit_path = os.path.join(root, timeunit_name)
                if not os.path.exists(timeunit_path):
                    os.makedirs(timeunit_path)

    def run(self):
        bug_id, time_unit = Bug2SumGenerator._get_dir_basename(self.root_folder).split('.')
        print('[INFO] Generating BugID: {}, Timeunit" {} ...'.format(bug_id, time_unit))
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
