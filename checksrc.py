#!/usr/bin/python

import sys
from util import *

def check_src(file):
    for line in lines(file):
#            d = line.split()
            d = line.strip()
            print d 
#            print line
    return True


check_src(sys.stdin)
