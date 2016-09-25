#!/usr/bin/env python

import sys
import getopt
import json


class Element:
    def __init__(self):
        self.name = None
        self.value = None
        self.children = None
"""
json format
{
  "name": "<name>",
  "value": <value>,
  "children": [
    <Object>
  ]
}
"""

def d3_extract(key):
    tmp = {}
    tmp["name"] = key.name
    tmp["value"] = key.value
    if (len(key.children.keys()) != 0):
        tmp["children"] =[]
        for key_tmp in key.children :
            tmp["children"].append(d3_extract(key.children[key_tmp]))
    return tmp

"""
The file should follow this format
Each line = one trace

"""
def parser_to_d3json(file_name, separator):
    f = open(file_name, 'r')
    count = {}
    for line in f:
        element = line.strip().split(separator)
        stack = "_".join(element)
        if stack not in count:
            count[stack] = 1
        else :
            count[stack] += 1

    root = {}
    current_list = root
    for key in count.keys():
        elements = key.split('_')
        current_list = root
        for element in elements:
            if element not in current_list :
                el = Element()
                el.name = element
                el.value = count[key]
                el.children = {}
                current_list[element] = el
                current_list = el.children;
            else :
                current_list[element].value += count[key]
                current_list = current_list[element].children

    output = []

    #fixme there is only one key to work"
    for key in root :
        output.append(d3_extract(root[key]))

    return output[0]


def usage():
    print "flame_graph_if.py stack_layers [separator]"

def main(argv):
    separator = ","
    try:
        opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-g':
            global _debug
            _debug = 1
        elif opt in ("-d", "--delimiter"):
            separator = arg

    source = "".join(args)
    print json.dumps(parser_to_d3json(source, separator))

if __name__ == "__main__":
    main(sys.argv[1:])
