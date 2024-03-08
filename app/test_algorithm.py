import random

def prepare_random_patient_data(disease_dict, num_diseases=1):
    """
    Prepare random patient data based on randomly selected diseases from the provided disease dictionary.

    Parameters:
    - disease_dict (dict): A dictionary containing information about different diseases.
    - num_diseases (int): The number of random diseases to select. Default is 1.

    Returns:
    - dict: A dictionary containing randomly selected patient data.
    
    The function selects a specified number of random diseases from the provided disease dictionary.
    For each selected disease, it extracts one value for each key from the disease information.
    If the key is 'nazwa objawu', multiple values may be randomly selected.
    The resulting patient data dictionary contains this extracted information.
    """

    # Select a specified number of random diseases
    random_disease_codes = random.sample(list(disease_dict.keys()), num_diseases)

    # Print the randomly selected disease codes
    print("=" * 50)
    print("Randomly selected disease codes:")
    for code in random_disease_codes:
        print(code)
        print("=" * 50)
    
    # Extract one value for each key from the randomly selected disease information
    patient_data = {}
    for code in random_disease_codes:
        disease_info = disease_dict[code]
        for key, value in disease_info.items():
            if key == 'nazwa objawu':
                # Randomly select multiple values for 'nazwa objawu'
                patient_data[key] = random.sample(value, random.randint(1, len(value)))
            elif key not in ['jednostka chorobowa', 'podgrupa chorób', 'grupa chorób']:
                # Ensure values are lists and select one value for other keys
                patient_data[key] = [random.choice(value)]
    
    return patient_data
