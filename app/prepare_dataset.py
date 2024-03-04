import pandas as pd
from itertools import product

def prepare_dataset(excel_file_path, remove_sheets, remove_columns=['Grupa objawów']):
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
        combinations_df["Sheet_Name"] = sheet_name

        # Append current sheet's DataFrame to combined DataFrame
        combined_df = pd.concat([combined_df, combinations_df], ignore_index=True)

    return combined_df
