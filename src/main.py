import os

from modules.chatGPT import ChatGPT
from modules.io_utils import write_json, json_obj


if __name__ == "__main__":
    openai_api_key = os.environ["OPENAI_API_KEY"]
    enable_json_output = True
    num_iterations = 5
    chunk_size = 4
    completion_file_path = "testing_data/json_data/test-1_completion.json"
    message_history_file_path = "testing_data/json_data/test-1_message_history.json"
    
    chat_gpt = ChatGPT(openai_api_key, enable_json_output=enable_json_output, chunk_size=chunk_size, completion_file_path=completion_file_path)

    for i in range(num_iterations):
        user_input = input("> ")
        print("User input was:", user_input)
        print(chat_gpt.chat(user_input))
        print()

    if chat_gpt.enable_json_output:
        conversation_summary = chat_gpt.generate_conversation_summary()
        data = json_obj(chat_gpt.message_history, conversation_summary)
        write_json(data, message_history_file_path)
    else:
        pass

