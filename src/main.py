import os
import datetime

from modules.chatGPT import chatbot_with_memory
from modules.io_utils import write_json


current_time = datetime.datetime.now()
current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
print(current_time)

json_data_filename = f"message_history_{current_time}.json"


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list


if __name__ == "__main__":
    message_history = chatbot_with_memory()
    flattened_history = reformat_nested_list(message_history)
    write_json(flattened_history, os.path.join("data/json_data", json_data_filename))
