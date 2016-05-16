import os
import json
import copy
import xmind
import argparse
from xmind.core.topic import TopicElement
from argparse import ArgumentDefaultsHelpFormatter


DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "output")
DEFAULT_SUMMARY_JSON_FN = "summary.json"
DEFAULT_SUMMARY_JSON_FP = os.path.join(DEFAULT_OUTPUT_DIR, DEFAULT_SUMMARY_JSON_FN)
DEFAULT_XMIND_FN = "summary.xmind"
DEFAULT_XMIND_FP = os.path.join(DEFAULT_OUTPUT_DIR, DEFAULT_XMIND_FN)
DEFAULT_SUMMARY_KEY = "summary"


class SummaryXmindGenerator(object):

    def __init__(self, input_fp=DEFAULT_SUMMARY_JSON_FP, output_fp=DEFAULT_XMIND_FP):
        self.input_fp = input_fp
        self.output_fp = output_fp

    def set_sub_key_element(self, input_data, sheet_obj, parent_topic):
        for sub_key in input_data:
            sub_key_element = TopicElement()  # create a new element
            sub_key_element.setTopicHyperlink(sheet_obj.getID())
            sub_key_element.setTitle(str(sub_key))
            parent_topic.addSubTopic(sub_key_element)
            if isinstance(input_data[sub_key], list) is False and isinstance(input_data[sub_key], unicode) is False:
                self.set_sub_key_element(input_data[sub_key], sheet_obj, sub_key_element)
            if isinstance(input_data[sub_key], unicode):
                sub_key_element.setPlainNotes(input_data[sub_key])

    def update_case_data(self, input_data, case_name):
            for sub_key in input_data:
                if isinstance(input_data[sub_key], list):
                    input_data[sub_key] = case_name
                else:
                    if isinstance(input_data[sub_key], unicode) is False:
                        self.update_case_data(input_data[sub_key], case_name)

    def deep_merge_dict(self, source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                self.deep_merge_dict(value, node)
            else:
                destination[key] = value

        return destination

    def merge_summary_data(self, summary_data):
        tmp_data = copy.deepcopy(summary_data)
        for case_name in tmp_data:
            self.update_case_data(tmp_data[case_name], case_name)
        case_name_list = tmp_data.keys()

        result_data = copy.deepcopy(tmp_data[case_name_list[0]])
        for case_name_index in range(1, len(case_name_list)):
            self.deep_merge_dict(tmp_data[case_name_list[case_name_index]], result_data)
        return result_data

    def generate_xmind(self):

        # merge sumamry data
        with open(self.input_fp) as summary_fh:
            summary_data = json.load(summary_fh)
        merged_summary_data = self.merge_summary_data(summary_data[DEFAULT_SUMMARY_KEY])

        # init xmind obj
        output_xmind_obj = xmind.load(self.output_fp)

        # create summary sheet
        summary_sheet = output_xmind_obj.getPrimarySheet()  # get the first sheet
        summary_sheet.setTitle(DEFAULT_SUMMARY_KEY)  # set its title
        root_topic = summary_sheet.getRootTopic()  # get the root topic of this sheet
        summary_root_key = merged_summary_data.keys()[0]
        root_topic.setTitle(summary_root_key)  # set its title
        self.set_sub_key_element(merged_summary_data[summary_root_key], summary_sheet, root_topic)

        # create case sheet
        if DEFAULT_SUMMARY_KEY in summary_data:
            for case_name in summary_data[DEFAULT_SUMMARY_KEY]:
                case_sheet = output_xmind_obj.createSheet()
                case_sheet.setTitle(case_name)
                case_root_topic = case_sheet.getRootTopic()
                root_key = summary_data[DEFAULT_SUMMARY_KEY][case_name].keys()[0]
                case_root_topic.setTitle(root_key)
                self.set_sub_key_element(summary_data[DEFAULT_SUMMARY_KEY][case_name][root_key], case_sheet,
                                         case_root_topic)
                output_xmind_obj.addSheet(case_sheet)
        else:
            print "The summary json file[%s] format is not correct!" % self.input_fp
        xmind.save(output_xmind_obj, self.output_fp)


def main():
    arg_parser = argparse.ArgumentParser(description='Summary Xmind Generator',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-i', action='store', dest='input_file_path', default=None,
                        help='summary json file path', required=False)
    arg_parser.add_argument('-o', action='store', dest='output_file_path', default=None,
                            help='xmind file path', required=False)
    args = arg_parser.parse_args()
    if args.input_file_path:
        if os.path.exists(args.input_file_path):
            run_obj = SummaryXmindGenerator(args.input_file_path, args.output_file_path)
            run_obj.generate_xmind()
        else:
            print "Please specify correct summary json file path!"
    else:
        run_obj = SummaryXmindGenerator()
        run_obj.generate_xmind()

if __name__ == '__main__':
    main()