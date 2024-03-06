from typing import List, Tuple

import pandas as pd

from app.crud import (
    SymptomsClient,
    SymptomDefinitionsClient,
    SymptomsValidationClient,
    DiseaseGroupDefinitionsClient
)



async def prepare_table(session, data, table_class, column_names: List[str],
                      columns_indexes_in_source_file: List[int]):
    """Funtion prepare data from dataframe to populate proper table in DB"""
    table_df = data.iloc[:, columns_indexes_in_source_file]
    table_df.drop_duplicates(ignore_index = True)
    table_df.dropna(how='all', inplace = True)
    table_df.where(table_df.notnull(), None, inplace = True)
    table_df.columns = column_names
    data_dict = table_df.to_dict('records')

    await table_class(session).populate_to_table(data_dict)


async def prepare_pseudo_symptoms_table(session, data, table_class, columns_indexes_in_source_file: List[int]):
    
    pseudo_symptoms_name = "pseudo_symptom_name"
    df_to_combine = data.iloc[:, columns_indexes_in_source_file]
    combined_df = pd.DataFrame({pseudo_symptoms_name:[]})
    for column in df_to_combine:
        df_to_append = df_to_combine[column].to_frame()
        df_to_append = df_to_append.drop_duplicates(ignore_index = True)
        df_to_append = df_to_append.dropna(how='all')
        df_to_append.columns = [pseudo_symptoms_name]
        combined_df = pd.concat([combined_df, df_to_append], ignore_index = True)
    combined_df.drop_duplicates(ignore_index = True, inplace = True)
    data_dict = combined_df.to_dict('records')

    await table_class(session).populate_to_table(data_dict)


async def read_xlsx_and_load_to_tables(input_file, session):
    """Function to read data from general sheet in excel"""

    general_data = pd.read_excel(input_file, sheet_name="General")
    # columns_indexes_in_source_file starting from 0
    # if you pass column name you have to proveide column index
    await prepare_pseudo_symptoms_table(session, general_data, SymptomsValidationClient, columns_indexes_in_source_file=[1,2,3,4,5,8,9,10,11,12])
    await prepare_table(session, general_data, SymptomDefinitionsClient, ['symptom_name'], columns_indexes_in_source_file=[1])
    await prepare_table(session, general_data, DiseaseGroupDefinitionsClient, ['disease_group_name'], columns_indexes_in_source_file=[8])
    