#!/usr/bin/env python
# -*- coding: utf-8 -*-

__app__ = "MultiStega"
__author__ = "Sanguinarius"
__credits__ = ""
__maintainer__ = "Sanguinarius"
__email__ = "sanguinarius.contact@gmail.com"
__version__ = "0.1"

# en entré nombre de message a chiffré path image , separateur


import argparse

from lib.action import *




parser = argparse.ArgumentParser(usage='%(prog)s -i InputFile (-H -o OutputFile [-n Number])|(-R) ')
parser.add_argument('-v', '--version', action="version", version="%s %s" %(__app__, __version__))

parser.add_argument('-i', '--inputfile', action="store", help="Input image source file", required=True)
parser.add_argument('-o', '--outputfile', action="store", help="output destination file")
parser.add_argument('-n', '--number', type=int, default=1, help="Number of messages (default=1)")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-H', '--hide', action='store_true', help="Active this option for hide"
                                                       " in file")
group.add_argument('-R', '--reveal', action='store_true', help="Active this option for"
                                                          " reveal message in file")

result = parser.parse_args()



arguments = dict(result._get_kwargs())
#print arguments

if arguments["hide"]== True and arguments["inputfile"]!= None and arguments["outputfile"]!= None:
    check_image(arguments["inputfile"])
    create = Write_Messages(arguments["inputfile"], arguments["outputfile"])
    create.create_message(arguments["number"])
elif arguments["reveal"]== True and arguments["inputfile"]!= None:
    check_image(arguments["inputfile"])
    reveal = Reveal_Messages(arguments["inputfile"])
    result = reveal.detect_message()
    for indice, item in enumerate(result):
        indice += 1
        print "Message %s : " % indice
        print item
else:
    parser.print_help()

