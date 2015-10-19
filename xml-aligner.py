#!/usr/bin/python
#
# generic XML prettifying ENGINE
# (spinoff from xml breadth-crawler)
"""
USAGE:  python xml-aligner.py <xml-document>[.xml]

"""
# TODO:
#   - run xmllint before running main `def` for input consistency
#   - polish regex 
#   - polish logic flow
#   - compartmentalize logic
#   - write unit tests ASAP
#   - make as generic as possible
#   - use class-based heirarchy

import sys
import re

def prettify(file):
    with open(file) as f:

        flag = False # true for when a 1st SC tag is encountered
        tags = []    # collector for SC tags
        margin = 0   # margin for the collected SC

        for line in f:
            if re.search(r'\/\>', line):

                if not flag:
                    flag = True
                    margin = len(line) - len(line.lstrip(' '))

                # gotta catch 'em all (SC tags)
                tags.append(line.strip())

            elif not flag:
                print line,

            # met when the group of SC tags end
            else:
                arrange(tags, margin)
                print line.rstrip()

                # reset
                del tags[:]
                flag = False
                margin = 0

def getKeys(tags):
    """ returns the keys of the group of SC Tags """

    keys = []

    for line in tags:
        for pair in re.findall(r'([a-z]*)\s*=\s*("[()\w\. ]*")', line):
            if pair[0] not in keys:
                keys.append(pair[0])

    keys.append('/>') # undecent hack for closing-tag
    return keys

def getMax(tags, key):

    max = 0

    # count max key position in tags
    for line in tags:
        if line.find(key) > max:
            max = line.find(key)

    return max

def arrange(tags = [], margin = 0):

    attrKeys = getKeys(tags)

    for key in attrKeys:
        max = getMax(tags, key)

        for i in range(len(tags)):
            if tags[i].find(key) > 0: 
                new = (max - tags[i].find(key))*' ' + key
                tags[i] = tags[i].replace(key, new)

    # damn that's pretty
    for line in tags:
        print (margin-1)*' ', line

if len(sys.argv) == 1:
    print "wrong"
    sys.exit()

prettify(sys.argv[1])
