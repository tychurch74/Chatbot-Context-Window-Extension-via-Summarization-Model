import os
import json


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        for item in sublist:
            flat_list.extend(item)
    return flat_list


def remove_non_dict_items(lst):
    new_lst = []
    for item in lst:
        if isinstance(item, dict):
            new_lst.append(item)
    return new_lst


def combine_json_files(folder_path, output_file_name):
    combined_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r") as f:
                data = json.load(f)

            combined_data.append(data)

    flattened_data = reformat_nested_list(combined_data)
    formatted_data = remove_non_dict_items(flattened_data)
    output_file_path = os.path.join("data", output_file_name)
    with open(output_file_path, "w") as output_file:
        json.dump(formatted_data, output_file, indent=2)


# Example usage
combine_json_files("data/json_data", "combined_data.json")
