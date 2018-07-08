#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# iba_to_raystation.py
"""
Import IBA OmniPro Accept CSV file into a RayStation compatible CSV
Created on Fri Apr 20 2018
@author: Dan Cutright, PhD
"""

from iba_to_python import IBA_Data


def iba_to_raystation(iba_file_path, raystation_file_path='rs.csv'):
    iba_data = IBA_Data(iba_file_path)

    text = []

    for i in range(0, len(iba_data.data)):
        text.append("# Dose Curve %s" % (i+1))
        text.append('# %s' % iba_data.date[i])

        unit_options = {'Photon': 'MV', 'Electron': 'MeV', 'Unknown': '?'}
        units = unit_options[iba_data.radiation_type[i]]
        energy = iba_data.energy[i].replace(units, '').strip()
        text.append("energy[%s]:; %s" % (units, energy))

        units = iba_data.ssd[i].split(' ')[-1]
        ssd = iba_data.ssd[i].replace(units, '').strip()
        text.append('SSD[%s]:; %s' % (units, ssd))

        units = iba_data.field_size[i].split(' ')[-1]
        field_size = iba_data.field_size[i].replace(units, '').strip()
        field_sizes = field_size.split(' x ')
        x = float(field_sizes[0])
        hx = x/2.
        y = float(field_sizes[1])
        hy = y/2.
        text.append('Fieldsize[%s]:; %s; %s; %s; %s;' % (units, -hx, -hy, hx, hy))

        curve_type = iba_data.scan_type[i].replace('Beam', 'Depth')
        text.append("CurveType:; %s" % curve_type)

        text.append("RadiationType:; %s" % iba_data.radiation_type[i])

        text.append("Medium:; %s" % iba_data.medium[i])

        text.append("Quantity:; RelativeDose")

        if iba_data.scan_type[i] == 'Beam':
            text.append("StartPoint[%s]:; 0; 0; 0" % iba_data.scan_units[i])
        elif iba_data.scan_type[i] in {'Inline', 'Crossline'}:
            z = iba_data.data[i]['z'][0]
            text.append("StartPoint[%s]:; 0; 0; %s" % (iba_data.scan_units[i], z))

        coord_options = {'Beam': 'z', 'Inline': 'y', 'Crossline': 'x'}
        coord = coord_options[iba_data.scan_type[i]]
        for j in range(0, len(iba_data.data[i]['x'])):
            text.append("%s; %s" %
                        (iba_data.data[i][coord][j],
                         iba_data.data[i]['value'][j]))

        text.append('End\n')

    with open(raystation_file_path, 'w') as rs:
        rs.write('\n'.join(text))
