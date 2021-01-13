#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 18:26:14 2020

@author: fas
"""

import pandas as pd
import numpy as np
import pydeck as pdk


def fix_str(string):
    string = string.replace(',', '.')
    return float(string)


def load_data(file, origin):

    if (origin == 'camtes'):

        # Read file
        df = pd.read_excel(file, index_col='IMO Number')

        # Deletes attribute rows at the end
        valid_indices = df.index.dropna()
        df = df.loc[valid_indices]
        df.reset_index(inplace=True)

        # Deletes unnecessary columns
        df.drop(['Reefer TEU', 'Latitude.1', 'Longitude.1'],
                axis=1, inplace=True)

        # Formats time
        df.DTG = pd.to_datetime(df.DTG, utc=True)

    elif (origin == 'seavision'):

        # Read file
        df = pd.read_excel(file, header=None)

        # Deletes original columns names
        df.drop(index=0, inplace=True)

        # Deletes unnecessary columns
        cols = np.arange(2, 106, step=2, dtype=int)
        df = df[cols]

        # Renames columns
        cols = {2: 'Latitude', 4: 'Longitude', 6: 'VesType', 8: 'ShipType',
                10: 'Status', 12: 'Speed', 14: 'Course', 16: 'Heading',
                18: 'MMSI', 20: 'IMO', 22: 'CallSign', 24: 'Length',
                26: 'Beam', 28: 'Draft', 34: 'Destination', 36: 'ETA',
                42: 'DTG', 64: 'Flag', 76: 'EEZ', 100: 'Name', 104: 'id'}
        df.rename(columns=cols, inplace=True)

        # Formats time
        df.DTG = pd.to_datetime(df.DTG)
        df['Latitude'] = df['Latitude'].astype('float64')
        df['Longitude'] = df['Longitude'].astype('float64')

    elif (origin == 'sat'):
        df = pd.read_csv(file)

        # Renames columns
        cols = {'LAT': 'Latitude', 'LON': 'Longitude'}
        df.rename(columns=cols, inplace=True)

        # Formats time
        df.DTG = pd.to_datetime(df.DTG, utc=True)

    return df


def create_Chart(chartType, df, color):

    layer = pdk.Layer(
        chartType,
        data=df,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["Longitude", "Latitude"],
        get_fill_color=color,
        get_line_color=color,
        tooltip="test test",
        )
    return layer
