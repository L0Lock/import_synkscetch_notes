# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Panel, Operator
from bpy.props import IntProperty, StringProperty
from rna_prop_ui import PropertyPanel
from bl_ui.utils import PresetPanel
from bpy_extras.io_utils import ImportHelper
import csv, textwrap, shutil, os

def _getCsvList():
    
    quote_character='"'
    delimiter=','

    if bpy.data.texts.get('SyncsketchComments') == None:
        return None

    with open(bpy.data.texts["SyncsketchComments"].filepath, "r") as csvFile:
        reader = csv.DictReader(csvFile, delimiter=delimiter, quotechar=quote_character, restkey='unrecognized_cols')
        csvList = list()
        for dictionary in reader:
            csvList.append(dictionary)
    return(csvList)

def _dpi_scale():
    return bpy.context.preferences.system.pixel_size

def _region_width():
    return bpy.context.region.width

def _char_width():
    rawWidth = _region_width()
    width = (rawWidth*0.9)/6
    
    # apply scale factor for retina screens etc
    width = int(width / _dpi_scale())
    # padding to account for some kerning
    # wrap = width/7
    
    return width

def _wrapper(textTowrap ):
    wrapp = textwrap.TextWrapper(_char_width(),)
    wrapList = wrapp.wrap(text=textTowrap) 
    
    return wrapList