#!/usr/bin/env python

import os
import re
import json
import argparse
from argparse import ArgumentDefaultsHelpFormatter

from time import gmtime, strftime, mktime
import datetime


class DatetimeConverter(object):
    TIME_STR_FORMAT = '%Y-%m-%dT%H:%M:%S'

    @staticmethod
    def get_UTC():
        return gmtime()

    @staticmethod
    def get_string_UTC():
        return strftime(DatetimeConverter.TIME_STR_FORMAT, gmtime())

    @staticmethod
    def get_datetime_from_string(input_time_string):
        return datetime.strptime(input_time_string, DatetimeConverter.TIME_STR_FORMAT)

    @staticmethod
    def get_timestamp_from_string(input_time_string):
        return mktime(DatetimeConverter.get_datetime_from_string(input_time_string).timetuple())


class SummaryGenerator(object):

    def __init__(self, root_folder):
        self.root_folder = root_folder

    def list_to_hierarchy_dict(self, dict_root, input_list):
        if input_list:
            node = input_list[0]
            if type(input_list[0]) is not str:
                node = str(input_list[0])
            current_node = dict_root.setdefault(node, {})
            self.list_to_hierarchy_dict(current_node, input_list[1:])

    def generate_summary_dict(self):
        ret_dict = {}
        for root, dirs, files in os.walk(self.root_folder):
            has_time = False
            time_list = []
            time_sum = 0
            time_counter = 0
            for f in files:
                if '.time' in f:
                    has_time = True
                    try:
                        t = int(re.sub(r'\.time(\.[0-9]+)?', '', f))
                        time_list.append(t)
                        time_sum += t
                        time_counter += 1
                    except Exception:
                        pass
            if has_time:
                # generate hierarchy dir dict from list
                dir_structure = root.split(os.sep)
                self.list_to_hierarchy_dict(ret_dict, dir_structure)

                # go to the inner dir
                cur_dir = ret_dict
                for next_dir in dir_structure:
                    cur_dir = cur_dir[next_dir]
                cur_dir[str(time_sum / time_counter)] = time_list
        return ret_dict

    def run(self):
        summary_dict = self.generate_summary_dict()
        utc_time = DatetimeConverter.get_string_UTC()
        summary_dict['UTC'] = utc_time
        print(json.dumps(summary_dict, indent=4))


def main():
    arg_parser = argparse.ArgumentParser(description='Summary Generator',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-d', '--dir', dest='root_folder', action='store', default='.',
                            help='the root folder', required=True)
    args = arg_parser.parse_args()
    sg = SummaryGenerator(args.root_folder)
    sg.run()

if __name__ == '__main__':
    main()
