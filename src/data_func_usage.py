import pandas as pd

from src.data.io_utils import (
    json_obj,
    write_json,
    add_to_json,
    resize_image,
    rgb_image_to_array,
    write_csv,
)

data_obj = json_obj(1, 2, 3)
file_name = "data/processed/test.json"
write_json(data_obj, file_name)
add_to_json(data_obj, file_name)

resize_image("data/raw/wallpaper 1.png", "data/processed/test_resized.png", (100, 100))
image = "data/processed/test_resized.png"
image_array = [rgb_image_to_array(image)]

image_labels = ["label1"]
data = pd.DataFrame({"label": image_labels, "pixel_data": image_array})
write_csv(data, "data/processed/test.csv")
