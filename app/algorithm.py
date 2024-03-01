import pandas as pd
from itertools import product
import os

# Excel file path
xls_file_path = os.path.join(os.getcwd(), r"data/data_template_polish_updated.xlsx")
print(xls_file_path)

# Initialize an empty DataFrame to store combined results
combined_df = pd.DataFrame()


# Read all sheets from the Excel file
all_data = pd.read_excel(xls_file_path, sheet_name=None)

del all_data["Objawy - ogólne"]

combined_df = pd.DataFrame()
# Iterate over each sheet
for sheet_name, data in all_data.items():
    # Collecting unique values for each column
    data_dict = {}
    for col in data.columns:
        unique_values = data[col].unique()

        # Exclude 'nan' values from unique_values
        unique_values = [value for value in unique_values if pd.notna(value)]
        data_dict[col] = unique_values

    # Fill empty lists with "NO"
    for col, values in data_dict.items():
        if not values:
            data_dict[col] = ["N/A"]

    # Generate all combinations of the rows
    combinations = list(product(*data_dict.values()))

    print(len(combinations))

    # Create list of dictionaries
    data_list = [dict(zip(data_dict.keys(), values)) for values in combinations]

    # Create DataFrame for current sheet
    combinations_df = pd.DataFrame(data_list)

    # Append a new column indicating the sheet name
    combinations_df["Sheet_Name"] = sheet_name

    # Append current sheet's DataFrame to combined DataFrame
    combined_df = pd.concat([combined_df, combinations_df], ignore_index=True)
