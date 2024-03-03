from typing import List, Tuple

import pandas as pd
import numpy as np

from app.crud import SymptomClient



async def prepare_table(session, data, table_class, column_names: List[str],
                      columns_indexes_in_source_file: List[int], split_by_bracket: bool = False):
    """Funtion prepare data from dataframe to populate proper table in DB"""
    number_of_columns = len(column_names)
    table_df = data.iloc[:, columns_indexes_in_source_file]
    table_df.drop_duplicates(ignore_index = True)
    table_df.dropna(how='all', inplace = True)
    table_df.replace(np.nan, '', regex=True, inplace = True)
    if number_of_columns > 1:
        table_df.columns = column_names
        data_list = table_df.to_dict('records')
    else:
        column_name = column_names[0]
        table_df.name = column_name
        table_list= table_df.to_list()
        data_list = [{column_name:v} for v in table_list]
    await table_class(session).populate_to_table(data_list)


async def read_xlsx_and_load_to_tables(input_file, session):
    """Function to read data from general sheet in excel"""

    all_data = pd.read_excel(input_file, sheet_name="Objawy - ogólne")
    # columns_indexes_in_source_file starting from 0
    # if you pass column name you have to proveide column index
    await prepare_table(session, all_data, SymptomClient, ['symptom_medical_name', 'symptom_description'], columns_indexes_in_source_file=[1,2])