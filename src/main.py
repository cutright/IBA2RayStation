#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# IBA2RS
"""
Import IBA OmniPro Accept CSV file into a RayStation compatible CSV
Created on Fri Apr 20 2018
@author: Dan Cutright, PhD
"""

from __future__ import print_function
from iba_to_raystation import iba_to_raystation as iba2rs
import os
import sys
from datetime import datetime


def main():

    if len(sys.argv) < 2:
        print("Please include the absolute file path of your IBA OmniPro Accept CSV.")
        return

    if not os.path.isfile(sys.argv[1]):
        print("Invalid file path: %s" % sys.argv[1])
        return

    file_path = sys.argv[1]

    if len(sys.argv) == 3:
        output_file = sys.argv[2]
    else:
        output_file = "RayStation_Beam_Data_%s.csv" % \
                      str(datetime.now()).replace(':', '-').replace(' ', '-').split('.')[0]

    iba2rs(file_path, output_file)


if __name__ == '__main__':
    main()
