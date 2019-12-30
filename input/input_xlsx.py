import pandas as pd

from input.convert_dict_types import convert_dict_types


def define_input_dict(input_file):
    dict_df = pd.read_excel(input_file, sheet_name=None, encoding="utf-16", dtype=object, index_col=None, header=0)
    input_dict = {}
    for (case, df) in dict_df.items():
        input_dict[str(case).lower()] = {}
        header = list(df.columns)
        for (index, row) in df.iterrows():
            list_row = list(row)
            input_dict[str(case).lower()][str(list_row[0])] = {}
            for (h, v) in zip(header[1:], list_row[1:]):
                input_dict[str(case).lower()][str(list_row[0])][str(h).lower()] = v
    input_dict = convert_dict_types(input_dict=input_dict)
    return input_dict
