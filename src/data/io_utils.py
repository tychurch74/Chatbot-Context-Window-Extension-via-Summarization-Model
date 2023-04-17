# io_utils.py
import pandas as pd
import numpy as np
import json
import os

from PIL import Image


def resize_image(image_path, output_path, size):
    # Resize an image to a specific pixel dimension
    with Image.open(image_path) as img:
        img_resized = img.resize(size, Image.ANTIALIAS)
        img_resized.save(output_path)


def grayscale_image_to_array(image_path):
    # Convert a grayscale image to numerical pixel data
    with Image.open(image_path) as img:
        img_gray = img.convert("L")
        pixel_data = np.asarray(img_gray, dtype=np.uint8)
    return pixel_data


def rgb_image_to_array(image_path):
    # Convert an RGB image to numerical pixel data
    with Image.open(image_path) as img:
        pixel_data = np.asarray(img, dtype=np.uint8)
    return pixel_data


def read_csv(file_path):
    # Read data from a CSV file
    return pd.read_csv(file_path)


def write_csv(data, file_path):
    # Write data to a CSV file
    data.to_csv(file_path, index=False)


def read_json(file_path):
    # Read data from a JSON file
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def json_obj(input1, input2):
    # Create a JSON object (modify this function to suit your needs)
    return {"message_history": input1, "sys_message": input2}


def write_json(data, file_path):
    # Write data to a JSON file
    with open(file_path, "w") as f:
        json.dump([data], f, indent=4)


def add_to_json(data, file_path):
    # Add data to a JSON file
    with open(file_path, "r") as f:
        json_data = json.load(f)
    json_data.append(data)
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)


def read_folder(folder_path, file_ext=None):
    # Read data from a folder with multiple files and return a list of file paths
    file_list = []
    for file_name in os.listdir(folder_path):
        if file_ext is None or file_name.endswith(file_ext):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
    return file_list


def save_folder(file_name, folder_path):
    # Save processed data into a folder with multiple files
    for i in file_name:
        os.path.join(folder_path, i)
