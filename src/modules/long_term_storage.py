import os
import json


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list


def combine_json_files(folder_path, output_file_name):
    combined_data = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Merge the data with the combined_data dictionary
            combined_data.append(data)

    # Write the combined_data dictionary to a new JSON file
    flattened_data = reformat_nested_list(combined_data)
    output_file_path = os.path.join(folder_path, output_file_name)
    with open(output_file_path, 'w') as output_file:
        json.dump(flattened_data, output_file, indent=2)

# Example usage
combine_json_files('data/json_data', 'combined_data.json')
