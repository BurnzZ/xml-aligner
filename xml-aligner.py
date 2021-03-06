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

# -------------------
# Flow:
# 
# prettify()
#   arrange() - called upon last SC tag
#       getMax()
#       clean()
#       ...
# -------------------

import json

import copy
import sys
import re

def prettify(file):
    """ Goes thru each line in the document and decides what to do with them. """

    with open(file) as f:

        startCapture = False # true for when a 1st SC tag is encountered
        tags         = []    # collector for SC tags
        margin       = 0     # margin for the collected SC

        for line in f:
            isTag     = re.search(r'\/\>', line)
            isComment = re.search(r'--\>', line)
            isEmpty   = line.strip()

            # skips empty lines
            if not isEmpty and not startCapture:
                print "\n",
                continue

            elif isTag or isComment or not isEmpty:

                # if not startCapture and ( not re.search(r'--\>', line) or not line.strip() ):
                if not startCapture:
                    startCapture = True
                    margin = len(line) - len(line.lstrip(' '))

                # gotta catch 'em all (SC tags)
                tags.append(line.strip())
    
            # prints lines as-is; since nothing started yet
            elif not startCapture:
                print line,

            # met when the group of SC tags end
            # this is where arrangement happens
            else:
                arrange(tags, margin)
                print line.rstrip()

                # reset
                del tags[:]
                startCapture = False
                margin = 0


def arrange(tags = [], margin = 0):
    """ Aligns to group of tags passed to it. """

    attrKeys, attrPairs = getKeys(tags)

    for key in attrKeys:

        tags = clean(tags, key, attrPairs)
        max = getMax(tags, key)

        for i in range(len(tags)):
            key_start = find(tags[i], key)
            
            if key_start > 0: 
                if key != '/>':
                    new = (max - key_start + 1)*' ' + key + ' '
                    tags[i] = tags[i].replace(' ' + key + ' ', new, 1)
                else:
                    new = (max - key_start)*' ' + key
                    tags[i] = tags[i].replace(key, new, 1)

    # print each line, with correct margin, and making sure it ain't empty
    for line in tags:
        if line.strip():
            print (margin-1)*' ', line
        else:
            print "\n",


def getMax(tags, key):
    """ Returns the max position of a given `key` (i.e. img, href) in a list of tags """

    max = 0

    # count max key position in tags
    for line in tags:
        if find(line, key) > max:
            max = find(line, key)

    return max

def find(tag, key, isKey = True, after = 0):
    """ prevents the bug in matching prematurely """

    if key != '/>':
        if isKey:
            regex = re.escape(key) + r"\s*="
        else:
            regex = r"=\s*" + re.escape(key)

        # check first if exists
        if not re.findall(regex, tag):
            return -1
        else:
            for match in re.finditer(regex, tag):
                if match.start() < after:
                    continue
                else:
                    position = match.start(0)
                    break
    else:
        position = tag.find(key)

    return position


def clean(tags, key, attrPairs):
    """ cleans and corrects whitespaces """
    # TODO: optimize code
    
    # removes repetitive whitespaces in a tag, particularly the ones before an attr-key
    for i in range(len(tags)):

        if (not tags[i]):
            continue

        pos = find(tags[i], key)

        # removes excess whitespaces by string shrinking
        while re.match(r'\s', tags[i][pos-2]):
            tags[i] = tags[i][:pos-2] + tags[i][pos-1:]
            pos = find(tags[i], key)

    # makes sure there's exactly one space in the '=' sign in between attr-key 
    for i in range(len(tags)):
        if key != '/>':
            endKey = find(tags[i], key) + len(key)

            if key in attrPairs[i].keys():
                startAttr = find(tags[i], attrPairs[i][key], False, endKey) + 1
            else:
                continue

            # removes excess whitespace after '=' sign 
            while re.match(r'\s', tags[i][startAttr]):
                tags[i] = tags[i][:startAttr] + tags[i][startAttr+1:]

            tags[i] = tags[i][:endKey] + ' = ' + tags[i][startAttr:]

    # makes sure there's an extra white space before the SC tag: '/>'
    if key == '/>':
        for i in range(len(tags)):
            start = tags[i].find(key)
            if start == -1:
                continue
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


if len(sys.argv) == 1:
    print "wrong"
    sys.exit()

prettify(sys.argv[1])
