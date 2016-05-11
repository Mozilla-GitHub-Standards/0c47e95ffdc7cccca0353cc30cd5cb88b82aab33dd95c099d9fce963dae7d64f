import os
import argparse
from argparse import ArgumentDefaultsHelpFormatter


class AsciiDiagGenerator(object):

    def __init__(self, input_dir_name):
        self.dir_name = input_dir_name

    def gen_data(self):
        result_dict = {}
        for root, dirs, files in os.walk(self.dir_name):
            if len(files) > 0:
                tmp_time = int(files[0].split(".")[0])
                tmp_percentage = ".".join(files[0].split(".")[1:]) + "%"
                new_level = root.replace(self.dir_name, '').count(os.sep)
                running_name = os.path.basename(root)
                parent_name = root.split(os.sep)[-2]
                if new_level in result_dict:
                    result_dict[new_level].append({"name": running_name, "time": tmp_time, "percentage": tmp_percentage, "parent": parent_name})
                else:
                    result_dict[new_level] = [{"name": running_name, "time": tmp_time, "percentage": tmp_percentage, "parent": parent_name}]
        return result_dict

    def paint(self, input_data, level, parent_name):
        indent = ((level)) * '|  ' + '|' + '-'
        if level in input_data:
            for paint_data in sorted(input_data[level], key=lambda x: x['time'], reverse=True):
                if paint_data['parent'] == parent_name or level == 0:
                    print('{s1:{c}^{n1}} {s2:{c}^{n2}} {s3} {s4}/'.format(s1=paint_data['time'], s2=paint_data['percentage'],
                                                                          c=" ", n1=5, n2=5,
                                                                          s3=indent, s4=paint_data['name']))
                    self.paint(input_data, level+1, paint_data['name'])

    def run(self):
        self.paint(self.gen_data(), 0, "")


def main():
    arg_parser = argparse.ArgumentParser(description='Ascii Diagram Generator',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-s', action='store', dest='search_dir_name', default=False,
                        help='folder need to generate ascii diagram', required=True)
    args = arg_parser.parse_args()
    run_obj = AsciiDiagGenerator(args.search_dir_name)
    run_obj.run()

if __name__ == '__main__':
    main()