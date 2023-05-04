import os

from modules.chatGPT import chatbot_with_memory
from modules.io_utils import write_json, json_obj


if __name__ == "__main__":
    message_history = chatbot_with_memory()
    write_json(message_history, os.path.join("testing_data", "message_history.json"))
