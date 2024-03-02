from typing import List, Tuple

from fastapi import Depends
import asyncio #is needed?
import pandas as pd
#from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.dialects.postgresql import insert

from app.models import Symptoms
from app.crud import populate_to_table


def prepare_table(data, table_class, column_names: List[str],
                      columns_indexes_in_source_file: Tuple[int], split_by_bracket: bool = False):
    """Funtion populates data from dataframe to proper table in DB"""
    number_of_columns = len(column_names)

    table_df = data[data.columns[columns_indexes_in_source_file]]
    table_df.drop_duplicates(ignore_index = True)
    table_df.dropna(inplace = True)
    if number_of_columns > 1:
        table_df.columns = column_names
        data_list = table_df.to_dict('records')
    else:
        column_name = column_names[0]
        table_df.name = column_name
        table_list= table_df.to_list()
        data_list = [{column_name:v} for v in table_list]

    asyncio.run(populate_to_table(table_class, data_list))


def read_xlsx_and_load_to_tables(input_file):
    """Function to read data from general sheet in excel"""

    all_data = pd.read_excel(input_file, sheet_name="Objawy - ogólne")
    prepare_table(all_data, Symptoms, ['symptom_medical_name'], columns_indexes_in_source_file=(1))