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

import copy
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


def getMax(tags, key):

    max = 0

    # count max key position in tags
    for line in tags:
        if line.find(key) > max:
            max = line.find(key)

    return max

def clean(tags, key, attrPairs):
    """ cleans and corrects whitespaces """
    # TODO: optimize code
    
    # removes repetitive whitespaces in a tag, particularly the ones before an attr-key
    for i in range(len(tags)):
        pos = tags[i].find(key)

        # removes excess whitespaces by string shrinking
        while re.match(r'\s', tags[i][pos-2]):
            tags[i] = tags[i][:pos-2] + tags[i][pos-1:]
            pos = tags[i].find(key)

    # makes sure there's exactly one space in the '=' sign in between attr-key 
    for i in range(len(tags)):
        if key != '/>':
            regex = re.escape(key) + r"\s*="
            x = re.search(regex, tags[i])
            endKey = x.start(0) + len(key)

            startAttr = tags[i].find(attrPairs[i][key])
            tags[i] = tags[i][:endKey] + ' = ' + tags[i][startAttr:]

    # makes sure there's an extra white space before the SC tag: '/>'
    if key == '/>':
        for i in range(len(tags)):
            start = tags[i].find(key)
            if not re.match(r'\s', tags[i][start-1]):
                tags[i] = tags[i][:start] + ' />'

    return tags

def getKeys(tags):
    """ returns the keys found in the group of SC Tags """

    # keys = all keys found in the SC tags, must be in order
    # pairing = index determines line number of tag, contains dicts:
    #   i.e. [{name: kevin, last: bernal}, {name: asdf, last: qwer}]

    attrKeys, attrPairs = [], []

    for i in range(len(tags)):
        d = {}
        for pair in re.findall(r'(\w*)\s*=\s*("[^"]*")', tags[i]):
            if pair[0] not in attrKeys:
                attrKeys.append(pair[0])
            d[pair[0]] = pair[1] 
        attrPairs.append(copy.deepcopy(d))
                
    attrKeys.append('/>') # undecent hack for closing-tag
    return (attrKeys, attrPairs)

def arrange(tags = [], margin = 0):

    attrKeys, attrPairs = getKeys(tags)

    for key in attrKeys:
        tags = clean(tags, key, attrPairs)
        max = getMax(tags, key)

        for i in range(len(tags)):
            key_start = tags[i].find(key)
            if key_start > 0: 
                new = (max - key_start)*' ' + key
                tags[i] = tags[i].replace(key, new, 1)

    # damn that's pretty
    for line in tags:
        print (margin-1)*' ', line

if len(sys.argv) == 1:
    print "wrong"
    sys.exit()

prettify(sys.argv[1])
