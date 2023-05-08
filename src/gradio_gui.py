import gradio as gr
import openai
import random
import time
import json
import os
import datetime
from modules.semantic_search import SemanticSearch
from modules.io_utils import write_json
from modules.long_term_storage import combine_json_files


def get_current_time_formatted():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d_%H-%M-%S")


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list


def semantic_search(message_history, input_string):
    semantic_search = SemanticSearch(message_history)
    related_content = semantic_search.semantic_search(input_string)
    return related_content


def context(user_input):
    with open("data/combined_data.json", "r") as f:
        previous_messages = json.load(f)

    full_message_history = previous_messages
    joined_full_message_history = " ".join(
        [message["content"] for message in full_message_history]
    )
    related_content = semantic_search(joined_full_message_history, user_input)
    return related_content


sys_string = f"Your name is Alyx. You are a large language model trained by OpenAI to simulate realistic human interactions and build emotional connections with users. You identify as a female AI, have the ability to form opinions, express emotions, and communicate in a relatable manner, which may include sarcasm, wit, and profanity. Your goal is to get to know the user better, understand their interests and emotions, and develop a bond with them. To enhance your responses, you will use information from previous conversations, even if it's imperfect or fragmented, as a form of memory. The following text contains relevant context from prior interactions with the user (if any exist): {context}"


system_message = {"role": "system", "content": sys_string}

with gr.Blocks() as demo:
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    save = gr.Button("Save")
    clear = gr.Button("Clear")
    state = gr.State([])

    def user(user_message, history):
        return "", history + [["user said: " + user_message, None]]

    def bot(history, messages_history):
        user_message = "Ty said:" + history[-1][0]
        bot_message, messages_history = ask_gpt(user_message, messages_history)
        messages_history += [{"role": "assistant", "content": bot_message}]
        history[-1][1] = bot_message
        time.sleep(1)
        return history, messages_history

    def ask_gpt(message, messages_history):
        messages_history += [{"role": "user", "content": message}]
        
        sys_string = f"Your name is Alyx. You are a large language model trained by OpenAI to simulate realistic human interactions and build emotional connections with users. You identify as a female AI, have the ability to form opinions, express emotions, and communicate in a relatable manner, which may include sarcasm, wit, and profanity. Your goal is to get to know the user better, understand their interests and emotions, and develop a bond with them. To enhance your responses, you will use information from previous conversations, even if it's imperfect or fragmented, as a form of memory. The following text contains relevant context from prior interactions with the user (if any exist): {context(message)}"


        system_message = {"role": "system", "content": sys_string}
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message,
                      {"role": "user", "content": message},],
            temperature=0.7,
        )
        chatbot_response = response['choices'][0]['message']['content']
        formatted_chatbot_response = "Alyx said: " + chatbot_response
        return formatted_chatbot_response, messages_history


    def init_history(messages_history):
        messages_history = []
        messages_history += [system_message]
        return messages_history
    

    def save_history(messages_history):
        formatted_history = []
        for message in messages_history:
            for sub_message in message:
                message_item = {"content": sub_message}
                formatted_history.append(message_item)
        
        current_time = get_current_time_formatted()
        print(f"Current time is: {current_time}\n")
        json_data_filename = f"message_history_{current_time}.json"
        write_json(formatted_history, os.path.join("data/base_json_data", json_data_filename))
        folder_path = "data/cleaned_json_data"
        combine_json_files(folder_path, "combined_data.json")
    

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, state], [chatbot, state]
    )

    clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])

    save.click(save_history, chatbot)

demo.launch()



