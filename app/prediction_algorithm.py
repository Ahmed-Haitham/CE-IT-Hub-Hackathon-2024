def exclude_diseases_based_on_excluding_sympthom(patient_data, disease_data):
    # print(patient_data['objawy wykluczające'])
    possible_diseases = []
    for disease_info in disease_data:
        # print(disease_info['objawy wykluczające'])
        if not(set(disease_info['objawy wykluczające'])&set(patient_data['objawy wykluczające'])):
            possible_diseases.append(disease_info)
    return possible_diseases

def exclude_diseases_based_on_dynamic(patient_data, disease_data):
    possible_diseases = []
    for disease_info in disease_data:
        if set(disease_info['nasilenie w czasie'])&set(patient_data['nasilenie w czasie']):
            possible_diseases.append(disease_info)
    return possible_diseases

def exclude_diseases_based_on_characteristic(patient_data, disease_data, feature):
    possible_diseases = []
    for disease_info in disease_data:
        if (set(disease_info[feature])&set(patient_data[feature]))or(disease_info[feature]==['N/A']):
            possible_diseases.append(disease_info)
    return possible_diseases


def predict_disease_excl(patient_data, disease_data_dict):
    disease_data = list(disease_data_dict.values())
    all_names = [d['jednostka chorobowa'][0] for d in disease_data]
    
    if 'objawy wykluczające' in list(patient_data.keys()):
        disease_data =exclude_diseases_based_on_excluding_sympthom(patient_data, disease_data)
    # print(len(disease_data))
    for feature in ['nazwa objawu', 'nasilenie w czasie', 'dynamika objawów', 'cechy objawu', 'wiek wystapienia pierwszych objawów','poziom ck']:
        if feature in list(patient_data.keys()):
            disease_data = exclude_diseases_based_on_characteristic(patient_data, disease_data, feature)
        # print(len(disease_data))

    if len(disease_data)==0:
        return {'grupa chorób': ['symptoms are not matching any disease'],
 'podgrupa chorób': ['symptoms are not matching any disease'],
 'jednostka chorobowa': ['symptoms are not matching any disease'],
 'diseases': dict(zip([i['jednostka chorobowa'][0] for i in list(disease_data_dict.values())], [0 for i in range(len(list(disease_data_dict.values())))]))}

    disease_names = [d['jednostka chorobowa'][0] for d in disease_data]

    disease_counter = [0]*len(disease_data)
    for key in patient_data.keys():
        for i, disease in enumerate(disease_data):
            if key in disease.keys():
                for item in patient_data[key]:
                    
                    if item in disease[key]:
                        disease_counter[i] += 1
                    elif not(item in disease[key]):

                        pass

    
    total_symptoms = sum(disease_counter)
    disease_probabilities = [round((count/total_symptoms)*100, 2) for count in disease_counter]
    max_index = disease_counter.index(max(disease_counter))
    predicted_disease = disease_data[max_index]['grupa chorób']

    # If patient provided enough data, predict 'podgrupa chorób' and 'jednostka chorobowa'.
    # If not, return predicted 'grupa chorób' with probabilities.
    probabilities_dict = dict(zip(list(disease_names), disease_probabilities))
    not_probable_diseases = set(all_names)-set(probabilities_dict.keys())

    probabilities_dict_joint = {**probabilities_dict, **dict(zip(list(not_probable_diseases), [0 for i in range(len(list(not_probable_diseases)))]))}
    probabilities_dict_sorted = dict(sorted(probabilities_dict_joint.items(), key=lambda item: item[1]))
    if set(['poziom ck', 'objawy obligatoryjne', 'objawy wykluczające', 'choroby współistniejące', 'cechy charakterystyczne i objawy współistniejące'])&(set(patient_data.keys())):
        
        return {'grupa chorób': predicted_disease, 'podgrupa chorób': disease_data[max_index]['podgrupa chorób'], 'jednostka chorobowa': disease_data[max_index]['jednostka chorobowa'], 'diseases': probabilities_dict_sorted}
    else:
        return {'grupa chorób': predicted_disease, 'probabilities': probabilities_dict_sorted}
    
def predict_disease(patient_data, disease_data_dict):
    disease_data = list(disease_data_dict.values())
    # Initializing counters for each diseases
    disease_counter = [0]*len(disease_data)
    for key in patient_data.keys():
        for i, disease in enumerate(disease_data):
            if key in disease.keys():
                for item in patient_data[key]:
                    if item in disease[key]:
                        # Increase counter if patient's symptoms match disease's symptoms
                        disease_counter[i] += 1
    
    total_symptoms = sum(disease_counter)
    disease_probabilities = [round((count/total_symptoms)*100, 2) for count in disease_counter]
    
    # Predict 'grupa chorób'
    max_index = disease_counter.index(max(disease_counter))
    predicted_disease = disease_data[max_index]['grupa chorób']

    disease_names = [d['jednostka chorobowa'][0] for d in disease_data]
    probabilities_dict = dict(zip(list(disease_names), disease_probabilities))
    probabilities_dict_sorted = dict(sorted(probabilities_dict.items(), key=lambda item: item[1]))

    # If patient provided enough data, predict 'podgrupa chorób' and 'jednostka chorobowa'.
    # If not, return predicted 'grupa chorób' with probabilities.
    if set(['poziom ck', 'objawy obligatoryjne', 'objawy wykluczające', 'choroby współistniejące', 'cechy charakterystyczne i objawy współistniejące'])&(set(patient_data.keys())):
        return {'grupa chorób': predicted_disease, 'podgrupa chorób': disease_data[max_index]['podgrupa chorób'], 'jednostka chorobowa': disease_data[max_index]['jednostka chorobowa'], 'probabilities': probabilities_dict_sorted}
    else:
        return {'grupa chorób': predicted_disease, 'probabilities': probabilities_dict_sorted}