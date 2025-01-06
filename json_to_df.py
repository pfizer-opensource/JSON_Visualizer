import os
import json
import pandas as pd
from datetime import datetime, timedelta
import pyreadstat as prs
import numpy as np
import jsonlines

def create_metadata(json_data):
    item_data = json_data['columns'][1:]
    # Creating metadata for XPT
    create_meta = {'label': {}, 'format': {}}
    for i in item_data:
        create_meta['label'][i['name']] = i['label']
        try:
            create_meta['format'][i['name']] = i['format']
        except KeyError:
            None
    return create_meta


def create_xpt(json_data):
    global decimal_list, date9_list, datetime20_list, xpt_filename
    columns_list = []
    for i in range(0, len(json_data['columns'])):
        columns_list.append(json_data['columns'][i]['name'])

    xpt_data = []
    for i in range(len(json_data['rows'])):
        xpt_data.append(dict(zip(columns_list, json_data['rows'][i])))

    create_meta = create_metadata(json_data)

    xpt_df = pd.DataFrame(xpt_data)
    return xpt_df

def ndjson_conversion(filepath):
    nd_data = {}
    with jsonlines.open(filepath) as reader:
        for i, obj in enumerate(reader):
            nd_data[i] = obj
    nd_dict = nd_data[0]
    row_list = []
    for i in range (1, len(nd_data.keys())):
        row_list.append(nd_data[i])
    nd_dict["rows"] = row_list
    return nd_dict




