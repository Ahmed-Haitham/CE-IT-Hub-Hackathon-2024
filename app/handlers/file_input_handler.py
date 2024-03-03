from typing import List, Tuple

import pandas as pd

from app.crud import SymptomClient, SymmetricityClient, DiseaseGroupClient, SymptomsDiseaseGroupClient, ProgressionClient, OnsetGroupClient, TestCkLevelClient



async def prepare_table(session, data, table_class, column_names: List[str],
                      columns_indexes_in_source_file: List[int], split_by_bracket: bool = False):
    """Funtion prepare data from dataframe to populate proper table in DB"""
    table_df = data.iloc[:, columns_indexes_in_source_file]
    table_df.drop_duplicates(ignore_index = True)
    table_df.dropna(how='all', inplace = True)
    table_df.where(table_df.notnull(), None, inplace = True)
    table_df.columns = column_names
    data_list = table_df.to_dict('records')

    await table_class(session).populate_to_table(data_list)


async def read_xlsx_and_load_to_tables(input_file, session):
    """Function to read data from general sheet in excel"""

    all_data = pd.read_excel(input_file, sheet_name="Objawy - ogólne")
    # columns_indexes_in_source_file starting from 0
    # if you pass column name you have to proveide column index
    await prepare_table(session, all_data, SymptomClient, ['symptom_medical_name'], columns_indexes_in_source_file=[1])
    await prepare_table(session, all_data, ProgressionClient, ['progression_name'], columns_indexes_in_source_file=[2])
    await prepare_table(session, all_data, SymmetricityClient, ['symmetricity_name'], columns_indexes_in_source_file=[3])
    await prepare_table(session, all_data, OnsetGroupClient, ['onset_group_name'], columns_indexes_in_source_file=[4])
    await prepare_table(session, all_data, TestCkLevelClient, ['test_ck_level_name'], columns_indexes_in_source_file=[7])
    await prepare_table(session, all_data, DiseaseGroupClient, ['disease_group_medical_name'], columns_indexes_in_source_file=[6])
    await prepare_table(session, all_data, SymptomsDiseaseGroupClient, ['symptom_id', 'disease_group_id'],
                        columns_indexes_in_source_file=[1,6])