import os
import json
import pandas as pd
from datetime import datetime, timedelta
import pyreadstat as prs
import numpy as np
import jsonlines


# def date_var(xpt_data):
#     # Format the date and datetime according to SAS time
#     # print(xpt_data)
#     for i in xpt_data:
#         for k, v in i.items():
#             # print(k, i[k],"*************")
#             if k in date9_list and i[k] != None and i[k] != '' and i[k].lower() != 'nat':
#                 date_string = i[k].split('T')[0]
#                 date_object = datetime.strptime(date_string, '%Y-%m-%d')
#                 sas_date_reference = datetime(1960, 1, 1)
#                 i[k] = (date_object - sas_date_reference).days
#             elif k in datetime20_list and i[k] != None and i[k] != '':
#                 sas_datetime_reference = datetime(1960, 1, 1, 00, 00, 00)
#                 datetime_object = datetime.strptime(i[k], "%Y-%m-%dT%H:%M:%S.%fZ")
#                 days_since_sas_ref = (datetime_object - sas_datetime_reference)
#                 i[k] = (days_since_sas_ref.days * 86400) + (days_since_sas_ref.seconds)
#             elif ((k in date9_list) or (k in datetime20_list)):
#                 if (type(i[k]) == "str" and i[k].lower() == 'nat') or (i[k] == None):
#                     i[k] = np.nan
#     return xpt_data
#
#
# def decimal_var(xpt_data):
#     for i in xpt_data:
#         for k, v in i.items():
#             if k in decimal_list and i[k] != '' and i[k] != None:
#                 i[k] = float(i[k])
#
#     return xpt_data

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
    # print(len(columns_list))

    xpt_data = []
    for i in range(len(json_data['rows'])):
        xpt_data.append(dict(zip(columns_list, json_data['rows'][i])))

    # decimal_list = []
    # date9_list = []
    # datetime20_list = []
    # for i in range(len(json_data['columns'])):
    #     if 'targetDataType' in json_data['columns'][i]:
    #         if json_data['columns'][i]['targetDataType'] == 'decimal':
    #             decimal_list.append(json_data['columns'][i]['name'])
    #         elif json_data['columns'][i]['targetDataType'] == 'integer':
    #             if json_data['columns'][i]['displayFormat'] == 'DATE9.':
    #                 # if json_data['columns'][i]['format'] == 'DATE9':
    #                 date9_list.append(json_data['columns'][i]['name'])
    #             if json_data['columns'][i]['displayFormat'] == 'DATETIME20.':
    #                 # if json_data['columns'][i]['format'] == 'DATETIME20':
    #                 datetime20_list.append(json_data['columns'][i]['name'])

    # xpt_data = date_var(xpt_data)
    # xpt_data = decimal_var(xpt_data)

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




