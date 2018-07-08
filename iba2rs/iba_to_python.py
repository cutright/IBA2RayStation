#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# iba_to_python.py
"""
Import IBA OmniPro Accept CSV file into a python object
Created on Fri Apr 20 2018
@author: Dan Cutright, PhD
"""

from dateutil.parser import parse
import numpy as np


class IBA_Data:
    def __init__(self, file_path):
        """
        From the csv file given, parse data into a python object
        :param file_path: absolute file_path of an IBA OmniPro Accept csv file
        """

        text = read_iba_file(file_path)
        indices = get_iba_data_indices(text)

        self.date = [text[d] for d in indices['date']]
        self.energy = [text[d+1].replace('Energy:;', '') for d in indices['description']]
        self.ssd = [text[d+7].replace('SSD:; ', '') for d in indices['description']]
        self.field_size = [text[d+8].replace('Field size:; ', '') for d in indices['description']]

        self.radiation_type = []
        for energy in self.energy:
            if energy.find('MV') > 0:
                self.radiation_type.append('Photon')
            elif energy.find('MeV') > 0:
                self.radiation_type.append('Electron')
            else:
                self.radiation_type.append('Unknown')

        self.medium = [text[d+10].replace('Measurement medium:; ', '') for d in indices['description']]
        self.scan_type = [text[d+11].replace('Scan type:; ', '') for d in indices['description']]

        self.scan_units = [text[d].replace('Points [', '').replace(']:', '') for d in indices['data_start']]

        self.data = []
        for i, j in enumerate(indices['data_start']):
            data_start = j+2
            data_end = indices['data_end'][i]

            data = {'x': [], 'y': [], 'z': [], 'value': []}
            if float(text[data_start].split('; ')[5]) == 0.:
                value_index = 3
            else:
                value_index = 5
            for k in range(data_start, data_end+1):
                row_data = text[k].split('; ')
                data['x'].append(row_data[1])
                data['y'].append(row_data[0])
                data['z'].append(row_data[2])
                data['value'].append(row_data[value_index])

            data = sort_data(data, self.scan_type[i])
            self.data.append(data)


def get_iba_data_indices(iba_text):
    """
    :param iba_text: a csv file exported from OmniPro Accept, split by new line characters into a list
    :return: a dictionary of starting indicies for a dataset's date, description, data start, and data end
    :rtype: dict
    """

    indices = {'date': [],
               'description': [],
               'data_start': [],
               'data_end': []}

    found = {'date': False,
             'description': False,
             'data': False}

    # iterate through each row of the text file, accumulate row index for each index type
    for i, row in enumerate(iba_text):
        if not found['date']:
            # if row can be automatically parsed as a date, it begins a new dataset
            try:
                parse(row)
                indices['date'].append(i)
                found['date'] = True
            except ValueError:
                pass

        elif not found['description']:
            if row != '':  # First non-empty line after date begins the description section
                indices['description'].append(i)
                found['description'] = True

        elif not found['data']:
            if row == '':  # first empty row after description indicates start of data
                indices['data_start'].append(i+1)
                found['data'] = True

        else:
            if row == '':  # empty row after data indicates end of data
                indices['data_end'].append(i-1)
                for key in list(found):
                    found[key] = False

    return indices


def read_iba_file(file_path):
    """
    :param file_path: absolute file path
    :return: a list of strings, each item being a row in the text file
    :rtype: list
    """
    f = open(file_path, 'r')
    text = f.read()
    return text.replace('\r', '').split('\n')


def sort_data(data, scan_type):
    """
    RayStation requires data to be in ascending order, whereas IBA exports in chronological order
    :param data: a dictionary of x, y, z, and values
    :param scan_type: per IBA, these could Beam, Inline, or Crossline, other options not supported by RayStation
    :return: a dictionary of x, y, z, and values sorted in ascending order by scan_type
    :rtype: dict
    """

    # Determine which coordinate to sort by
    sort_by = {'Beam': 'z', 'Inline': 'y', 'Crossline': 'x'}[scan_type]

    # Use numpy to sort data, which is stored as strings, covert to float before sorting, returned data still string
    sort_me_str = np.array(data[sort_by])
    sort_me_float = sort_me_str.astype(np.float)
    sorted_indices = np.argsort(sort_me_float)

    # create new dictionary of data, sorted by sorted_indices
    new_data = {'x': [], 'y': [], 'z': [], 'value': []}
    for var in list(new_data):
        new_data[var] = [data[var][sorted_indices[i]] for i in range(0, len(sorted_indices))]

    # RayStation does not allow repeated coordinates
    # Determine repeated indices
    repeated_indices = []
    for i in range(0, len(sorted_indices)):
        if new_data[sort_by][i] in new_data[sort_by][0:i]:  # Check only current index and earlier
            repeated_indices.append(i)
    # Remove repeated indices
    for i in repeated_indices[::-1]:
        for var in {'x', 'y', 'z', 'value'}:
            new_data[var].pop(i)

    return new_data
