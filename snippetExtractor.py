#! /usr/bin/env python3
import sys, os
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(MAIN_DIR, ".."))
#----------------------------------------------------------------------------------------------------------------------



from os.path import expanduser
import configparser

#Constants
TAB = " " * 4
#Config
CONFIG_FILE_NAME = "config.ini"
CONFIG_SECTION_1 = "CrawlSettings"
CONFIG_SECTION_1_ROOT = "root"
CONFIG_SECTION_1_TYPE = "snippet_type"
CONFIG_SECTION_1_PREFIX = "snippet_prefix"
CONFIG_SECTION_1_OUTPUT = "output"
CONFIG_SECTION_1_FILES = "file_types"
CONFIG_SECTION_1_IGNORE_DIR = "folder_ignore"
CONFIG_SPLIT_SYMBOL = '|'


#Get settings
config = configparser.ConfigParser()
config.read(os.path.join(MAIN_DIR, CONFIG_FILE_NAME))

#get dir to walk through
root = config[CONFIG_SECTION_1][CONFIG_SECTION_1_ROOT]
if(root == "."):
    root = MAIN_DIR

#get type and prefix
snippet_type = config[CONFIG_SECTION_1][CONFIG_SECTION_1_TYPE]
snippet_prefix = config[CONFIG_SECTION_1][CONFIG_SECTION_1_PREFIX]
#get file types to parse to
file_types = config[CONFIG_SECTION_1][CONFIG_SECTION_1_FILES].split(CONFIG_SPLIT_SYMBOL)
#get directories to ignore to
folder_ignore = config[CONFIG_SECTION_1][CONFIG_SECTION_1_IGNORE_DIR].split(CONFIG_SPLIT_SYMBOL)
#get output filename
output = config[CONFIG_SECTION_1][CONFIG_SECTION_1_OUTPUT]

def readFile(file):
    with open(file, 'r') as file_reader:
        return file_reader.read()

def print_snippet(file_writer, input_file, name):
    file_writer.write(TAB)
    file_writer.write("'" + name + "':\n")
    file_writer.write(TAB*2)
    file_writer.write("'prefix': '" + snippet_prefix + name + "'\n")
    file_writer.write(TAB*2)
    file_writer.write("'body': '''" + readFile(input_file) + "'''\n")
    file_writer.write("\n\n")

with open(output, 'w') as file_writer:

    file_writer.write("'" + snippet_type + "':\n")

    for dirname, subdirs, files in os.walk(root):
        # print path to all filenames.
        for file in files:
            (name, ext) = os.path.splitext(file)
            if ext in file_types:
                print_snippet(file_writer, os.path.join(dirname, file), name)

        #remove directories not to walk through
        for dir in folder_ignore:
            if dir in subdirs:
                subdirs.remove(dir)

