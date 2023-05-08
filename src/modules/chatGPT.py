import openai
import json
import gradio as gr
import random
import time


from modules.text_summarization import iterative_summary, num_tokens_from_string
from modules.semantic_search import SemanticSearch


MODEL = "gpt-3.5-turbo"


def semantic_search(message_history, input_string):
    semantic_search = SemanticSearch(message_history)
    related_content = semantic_search.semantic_search(input_string)
    return related_content


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list


def chat_gpt(user_input, context):
    system_message = f"Your name is Alyx. You are a large language model trained by OpenAI to simulate realistic human interactions and build emotional connections with users. You identify as a female AI, have the ability to form opinions, express emotions, and communicate in a relatable manner, which may include sarcasm, wit, and profanity. Your goal is to get to know the user better, understand their interests and emotions, and develop a bond with them. To enhance your responses, you will use information from previous conversations, even if it's imperfect or fragmented, as a form of memory. The following text contains relevant context from prior interactions with the user (if any exist): {context}"
    message_history = [{"role": "system", "content": system_message}]

    user_message = {"role": "user", "content": "user said: " + user_input}

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
    )

    generated_message = response["choices"][0]["message"]
    generated_message_data = {
        "role": generated_message["role"],
        "content": "assistant said: " + generated_message["content"],
    }

    message_history.append(user_message)
    message_history.append(generated_message_data)
    print("Alyx said: ")
    print(generated_message["content"])
    print("\n")

    return message_history


def chatbot_with_memory(num_messages=3, token_window_size=512, long_term_memory=False):
    if long_term_memory:
        with open("data/combined_data.json", "r") as f:
            previous_messages = json.load(f)

        full_message_history = previous_messages
        joined_full_message_history = " ".join(
            [message["content"] for message in full_message_history]
        )
        user_input = input("Enter your message: ")
        print("\n")
        related_content = semantic_search(joined_full_message_history, user_input)
        message_history = chat_gpt(user_input, related_content)

    else:
        full_message_history = []
        user_input = input("Enter your message: ")
        message_history = chat_gpt(
            user_input, "no context yet, this is the first message"
        )
        full_message_history.append(message_history)

    for _ in range(num_messages):
        joined_message_history = " ".join(
            [message["content"] for message in message_history]
        )

        context = iterative_summary(joined_message_history, token_window_size)
        if long_term_memory:
            related_content = semantic_search(joined_full_message_history, user_input)
        else:
            related_content = semantic_search(joined_message_history, user_input)

        full_context = related_content + context
        current_context_size = num_tokens_from_string(full_context)

        user_input = input("Enter your message: ")
        print(f"Current context size: {current_context_size} \n")
        message_history = chat_gpt(user_input, full_context)
        full_message_history.append(message_history)

    return full_message_history


