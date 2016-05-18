import os
import json
import copy
import xmind
import zipfile
import argparse
from xmind.core import const
from xmind.core.topic import TopicElement
from argparse import ArgumentDefaultsHelpFormatter


DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "output")
DEFAULT_SUMMARY_JSON_FN = "summary.json"
DEFAULT_SUMMARY_JSON_FP = os.path.join(DEFAULT_OUTPUT_DIR, DEFAULT_SUMMARY_JSON_FN)
DEFAULT_XMIND_FN = "summary.xmind"
DEFAULT_XMIND_FP = os.path.join(DEFAULT_OUTPUT_DIR, DEFAULT_XMIND_FN)
DEFAULT_SUMMARY_KEY = "summary"

DEFAULT_EXT_TIMEUNIT = '.timeunit'
DEFAULT_STYLE_LIGHTBLUE = '2jl4ip5e1us6tbs0lqs1krlt2l'
DEFAULT_STYLE_RED = '7qiv4j6tps0jcvi2p7b1hpc584'
DEFAULT_STYLE_BLOD = '5kbl9k0fde1f46i1q3deoej19d'
DEFAULT_THEME = 'xminddefaultthemeid'
DEFAULT_STYLE_PATH = 'styles.xml'
DEFAULT_MANIFEST_PATH = 'META-INF/manifest.xml'
DEFAULT_STYLE_FILE = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xmap-styles xmlns="urn:xmind:xmap:xmlns:style:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:svg="http://www.w3.org/2000/svg" version="2.0">
    <master-styles>
        <style id="xminddefaultthemeid" name="%Professional" type="theme">
            <theme-properties>
                <default-style style-family="summary" style-id="7d9kt3gnubosn6kg9rmssmq840"/>
                <default-style style-family="relationship" style-id="5fhi0g3uqonmhu22d4maq7futh"/>
                <default-style style-family="centralTopic" style-id="3mdd4fat7enea7r8u5bpqvshai"/>
                <default-style style-family="calloutTopic" style-id="0m7fapur4mp7l69rl6sao2e5n4"/>
                <default-style style-family="map" style-id="3ltr70o4bmouqv869u4ee7e0fr"/>
                <default-style style-family="subTopic" style-id="553ra1b7s1r1lfg60afmf05iin"/>
                <default-style style-family="floatingTopic" style-id="1lnhqq8a3ls241d9ai5qjhrajf"/>
                <default-style style-family="mainTopic" style-id="6404dq55olue08p1d0lbcj002c"/>
                <default-style style-family="boundary" style-id="6mfecvlsntgtrhm3f7j9o904ko"/>
                <default-style style-family="summaryTopic" style-id="7a76ihfnjsosqk40vjavfnvfbr"/>
            </theme-properties>
        </style>
    </master-styles>
    <automatic-styles>
        <style id="7d9kt3gnubosn6kg9rmssmq840" type="summary">
            <summary-properties line-color="#3076DC" line-width="1pt" shape-class="org.xmind.summaryShape.curly"/>
        </style>
        <style id="5fhi0g3uqonmhu22d4maq7futh" type="relationship">
            <relationship-properties arrow-end-class="org.xmind.arrowShape.triangle" fo:color="#595959" fo:font-family="Georgia" fo:font-size="10pt" fo:font-style="italic" fo:font-weight="normal" fo:text-decoration="none" line-color="#B62C25" line-pattern="dash" line-width="3pt"/>
        </style>
        <style id="3mdd4fat7enea7r8u5bpqvshai" type="topic">
            <topic-properties border-line-color="#3D537F" border-line-width="1pt" fo:font-family="Open Sans" line-class="org.xmind.branchConnection.curve" line-color="#7F7F7F" line-width="1pt" shape-class="org.xmind.topicShape.roundedRect" svg:fill="#CADDFE"/>
        </style>
        <style id="0m7fapur4mp7l69rl6sao2e5n4" type="topic">
            <topic-properties border-line-color="#F1BD51" border-line-width="1pt" fo:font-family="Open Sans" svg:fill="#FBF09C"/>
        </style>
        <style id="3ltr70o4bmouqv869u4ee7e0fr" type="map">
            <map-properties color-gradient="none" line-tapered="none" multi-line-colors="none" svg:fill="#FFFFFF"/>
        </style>
        <style id="553ra1b7s1r1lfg60afmf05iin" type="topic">
            <topic-properties fo:font-family="Open Sans"/>
        </style>
        <style id="1lnhqq8a3ls241d9ai5qjhrajf" type="topic">
            <topic-properties border-line-width="0pt" fo:color="#FFFFFF" fo:font-family="Open Sans" fo:font-weight="bold" svg:fill="#7F7F7F"/>
        </style>
        <style id="6404dq55olue08p1d0lbcj002c" type="topic">
            <topic-properties border-line-color="#8D867E" border-line-width="1pt" fo:font-family="Open Sans" shape-class="org.xmind.topicShape.roundedRect" svg:fill="#FEF4EC"/>
        </style>
        <style id="6mfecvlsntgtrhm3f7j9o904ko" type="boundary">
            <boundary-properties fo:color="#FFFFFF" fo:font-family="Georgia" fo:font-size="10pt" fo:font-style="italic" line-color="#4583C2" line-pattern="solid" line-width="1pt" shape-class="org.xmind.boundaryShape.roundedPolygon" svg:fill="#4583C2" svg:opacity=".2"/>
        </style>
        <style id="7a76ihfnjsosqk40vjavfnvfbr" type="topic">
            <topic-properties border-line-width="0pt" fo:color="#FFFFFF" fo:font-family="Georgia" fo:font-size="10pt" fo:font-style="italic" shape-class="org.xmind.topicShape.roundedRect" svg:fill="#2A70D9"/>
        </style>
    </automatic-styles>
    <styles>
        <style id="2jl4ip5e1us6tbs0lqs1krlt2l" type="topic"><topic-properties fo:color="#3366FF"/></style>
        <style id="7qiv4j6tps0jcvi2p7b1hpc584" type="topic"><topic-properties fo:color="#FF0303"/></style>
        <style id="5kbl9k0fde1f46i1q3deoej19d" type="topic"><topic-properties fo:font-weight="bold"/></style>
    </styles>
</xmap-styles>
"""
DEFAULT_MANIFEST_FILE = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">
    <file-entry full-path="content.xml" media-type="text/xml"/>
    <file-entry full-path="META-INF/" media-type=""/>
    <file-entry full-path="META-INF/manifest.xml" media-type="text/xml"/>
    <file-entry full-path="styles.xml" media-type=""/>
</manifest>
"""


class SummaryXmindGenerator(object):
    def __init__(self, input_fp=DEFAULT_SUMMARY_JSON_FP, output_fp=DEFAULT_XMIND_FP):
        self.input_fp = input_fp
        self.output_fp = output_fp

    def set_sub_key_element(self, input_data, sheet_obj, parent_topic):
        for sub_key in input_data:
            sub_key_element = TopicElement()  # create a new element
            sub_key_element.setTopicHyperlink(sheet_obj.getID())
            sub_key_element.setTitle(str(sub_key))
            if str(sub_key).endswith(DEFAULT_EXT_TIMEUNIT):
                sub_key_element.setAttribute(const.ATTR_STYLE_ID, DEFAULT_STYLE_LIGHTBLUE)
            elif str(sub_key).isdigit():
                sub_key_element.setAttribute(const.ATTR_STYLE_ID, DEFAULT_STYLE_RED)
            parent_topic.addSubTopic(sub_key_element)
            if isinstance(input_data[sub_key], dict):
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

    def append_xmind_style(self):
        with zipfile.ZipFile(self.output_fp, "a") as xmind_file:
            xmind_file.writestr(DEFAULT_STYLE_PATH, DEFAULT_STYLE_FILE)
            xmind_file.writestr(DEFAULT_MANIFEST_PATH, DEFAULT_MANIFEST_FILE)

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
        summary_sheet.setAttribute(const.ATTR_THEME, DEFAULT_THEME)
        root_topic = summary_sheet.getRootTopic()  # get the root topic of this sheet
        summary_root_key = merged_summary_data.keys()[0]
        root_topic.setTitle(summary_root_key)  # set its title
        self.set_sub_key_element(merged_summary_data[summary_root_key], summary_sheet, root_topic)

        # create case sheet
        if DEFAULT_SUMMARY_KEY in summary_data:
            for case_name in summary_data[DEFAULT_SUMMARY_KEY]:
                case_sheet = output_xmind_obj.createSheet()
                case_sheet.setTitle(case_name)
                case_sheet.setAttribute(const.ATTR_THEME, DEFAULT_THEME)
                case_root_topic = case_sheet.getRootTopic()
                root_key = summary_data[DEFAULT_SUMMARY_KEY][case_name].keys()[0]
                case_root_topic.setTitle(root_key)
                self.set_sub_key_element(summary_data[DEFAULT_SUMMARY_KEY][case_name][root_key], case_sheet,
                                         case_root_topic)
                output_xmind_obj.addSheet(case_sheet)
        else:
            print "The summary json file[%s] format is not correct!" % self.input_fp
        xmind.save(output_xmind_obj, self.output_fp)
        self.append_xmind_style()


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
