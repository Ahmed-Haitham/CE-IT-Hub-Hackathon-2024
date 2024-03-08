import pandas as pd
from itertools import product

def combine_dataset(excel_file_path, remove_sheets, remove_columns=['Grupa objawów']):
    """
    Prepare a combined dataset from an Excel file by removing specified sheets and columns.

    Args:
        excel_file_path (str): Path of the Excel file.
        remove_sheets (list): List of sheet numbers to be removed from the Excel file.
        remove_columns (list, optional): List of column names to be removed from each sheet.
            Defaults to ['Grupa objawów'].

    Raises:
        TypeError: If 'remove_sheets' argument is not a list.
        TypeError: If 'remove_columns' argument is not a list.

    Returns:
        pandas.DataFrame: Prepared dataset combining the data sheets and columns.
    """

    # Warning if remove_sheets is not a list
    if not isinstance(remove_sheets, list):
        raise TypeError("The 'remove_sheets' argument should be a list of sheet numbers to be removed.")

    # Warning if remove_columns is not a list
    if not isinstance(remove_columns, list):
        raise TypeError("The 'remove_columns' argument should be a list of column names to be removed from each sheet.")

    # Read all sheets from the Excel file
    all_data = pd.read_excel(excel_file_path, sheet_name=None)

    # Remove sheets from the Excel file based on 'remove_sheets' input
    indices_to_remove = [x - 1 for x in remove_sheets]
    items_list = list(all_data.items())
    updated_items_list = [item for i, item in enumerate(items_list) if i not in indices_to_remove]
    all_data_updated = dict(updated_items_list)

    # Iterate over each sheet
    combined_df = pd.DataFrame()
    for sheet_name, data in all_data_updated.items():

        # Remove columns from each sheet based on 'remove_columns' input
        for col in remove_columns:
            if col in data.columns:
                data.pop(col)

        # Collect unique values for each column
        data_dict = {}
        for col in data.columns:
            unique_values = data[col].unique()

            # Exclude 'nan' values from unique_values
            unique_values = [value for value in unique_values if pd.notna(value)]
            data_dict[col] = unique_values

        # Fill empty lists with "N/A"
        for col, values in data_dict.items():
            if not values:
                data_dict[col] = ["N/A"]

        # Generate all combinations of the rows
        combinations = list(product(*data_dict.values()))

        # Create list of dictionaries
        data_list = [dict(zip(data_dict.keys(), values)) for values in combinations]

        # Create DataFrame for the current sheet
        combinations_df = pd.DataFrame(data_list)

        # Append a new column indicating the sheet name
        combinations_df["disease_code"] = sheet_name

        # Append current sheet's DataFrame to combined DataFrame
        combined_df = pd.concat([combined_df, combinations_df], ignore_index=True)

    return combined_df


def convert_excel_to_long_format(excel_file_path, remove_sheets, remove_columns):
    """
    Prepare a long dataset from an Excel file and removing specified sheets and columns.

    Args:
        excel_file_path (str): Path of the Excel file.
        remove_sheets (list): List of sheet numbers to be not included in the long data.
        remove_columns (list): List of column names to be not included in the long data.

    Raises:
        TypeError: If 'remove_sheets' argument is not a list.
        TypeError: If 'remove_columns' argument is not a list.
        ValueError: If the Excel file contains one or more empty sheets that are not included in the 'remove_sheets' argument.

    Returns:
        pandas.DataFrame: Prepared long dataset with specified the data sheets and columns.
    """

    # Warning if remove_sheets is not a list
    if not isinstance(remove_sheets, list):
        raise TypeError("The 'remove_sheets' argument should be a list of sheet numbers to be not included in the long data.")

    # Warning if remove_columns is not a list
    if not isinstance(remove_columns, list):
        raise TypeError("The 'remove_columns' argument should be a list of column names to be not included in the long data.")
    
    # Read all sheets from the Excel file
    all_data = pd.read_excel(excel_file_path, sheet_name=None)

    # Get the index of the empty sheets
    empty_sheet_indices = [i for i, data in enumerate(all_data.values()) if data.empty]

    # Add 1 to each index in empty_sheet_indices
    empty_sheet_indices = [index + 1 for index in empty_sheet_indices]

    # Check if any sheet is empty
    if empty_sheet_indices:
        # Check if empty_sheet_indices contains any values not present in remove_sheets
        if any(index not in remove_sheets for index in empty_sheet_indices):
            raise ValueError("The Excel file contains one or more empty sheets that are not included in the 'remove_sheets' argument.")

    # Remove sheets from the Excel file based on 'remove_sheets' input
    indices_to_remove = [x - 1 for x in remove_sheets]
    items_list = list(all_data.items())
    updated_items_list = [item for i, item in enumerate(items_list) if i not in indices_to_remove]
    all_data_updated = dict(updated_items_list)

    # Iterate over each sheet
    all_diseases_long = pd.DataFrame()
    for sheet_name, data in all_data_updated.items():
        # Collect unique values for each column
        data_dict = {}
        for col in data.columns:
            unique_values = data[col].unique()
            # Exclude 'nan' values from unique_values
            unique_values = [value for value in unique_values if pd.notna(value)]
            data_dict[col] = unique_values

        # Fill empty lists with "N/A"
        for col, values in data_dict.items():
            if not values:
                data_dict[col] = ["N/A"]

        symptom_categories = []
        symptoms = []

        for category, values in data_dict.items():
            for value in values:
                symptom_categories.append(category)
                symptoms.append(value)

        long_df = pd.DataFrame({'symptom': symptoms, 'symptom_category': symptom_categories})
        long_df['disease'] = data_dict['jednostka chorobowa'][0]

        # Remove values from symptom_category column
        long_df = long_df[~long_df['symptom_category'].isin(remove_columns)].reset_index(drop=True)
        
        # Append a new column indicating the sheet name
        long_df["disease_code"] = sheet_name

        # Append current sheet's DataFrame to combined DataFrame
        all_diseases_long = pd.concat([all_diseases_long, long_df], ignore_index=True)

    return all_diseases_long


def convert_long_to_dictionary(long_dict):
    """
    Converts a long-format DataFrame into a nested dictionary.

    Parameters:
    - long_df (DataFrame): Input long DataFrame.

    Returns:
    - dict_all (dict): Nested dictionary where keys are disease codes and values are dictionaries
                     containing symptom categories as keys and lists of symptoms as values.
    """
    long_df = pd.DataFrame(long_dict)
    dict_all = {}
    grouped_df = long_df.groupby('disease_code')
    for disease_code, group_df in grouped_df:
        disease_symptoms = {}
        for _, row in group_df.iterrows():
            category = row['symptom_category']
            symptom = row['symptom_name']
            if category not in disease_symptoms:
                disease_symptoms[category] = []
            disease_symptoms[category].append(symptom)
        dict_all[disease_code] = disease_symptoms
    return dict_all

