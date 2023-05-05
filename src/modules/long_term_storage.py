import os
import json


def remove_non_dict_items(json_data):
    for sublist in json_data:
        return [item for item in sublist if isinstance(item, dict)]


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list


def process_json_files(folder_path="data/base_json_data"):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            cleaned_data = remove_non_dict_items(data)
            output_file_path = os.path.join('data/cleaned_json_data', file_name)
            with open(output_file_path, 'w') as output_file:
                json.dump(cleaned_data, output_file, indent=2)


def remove_additional_system_dicts(data):
    seen_system = False
    result = []

    for d in data:
        if d.get('role') == 'system':
            if not seen_system:
                seen_system = True
                result.append(d)
        else:
            result.append(d)

    return result


def combine_json_files(folder_path, output_file_name):
    process_json_files()
    combined_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r") as f:
                data = json.load(f)

            combined_data.append(data)
    formated_list = reformat_nested_list(combined_data)
    formated_list = remove_additional_system_dicts(formated_list)
    output_file_path = os.path.join("data", output_file_name)
    with open(output_file_path, "w") as output_file:
        json.dump(formated_list, output_file, indent=2)


