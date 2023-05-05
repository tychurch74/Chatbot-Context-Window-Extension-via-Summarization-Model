import openai
import json

from modules.text_summarization import iterative_summary
from modules.semantic_search import SemanticSearch


MODEL = "gpt-3.5-turbo"


def chat_gpt(user_input, context):
    system_message = f"You are a helpful assistant. Use the following context to help inform your responses: {context}"
    message_history = [{"role": "system", "content": system_message}]

    user_message = {"role": "user", "content": "user said: " + user_input}

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
    )

    generated_message = response["choices"][0]["message"]
    generated_message_data = {
        "role": generated_message["role"],
        "content": "assistant said: " + generated_message["content"],
    }

    message_history.append(user_message)
    message_history.append(generated_message_data)
    print(generated_message["content"])

    return message_history


def semantic_search(message_history, input_string):
    semantic_search = SemanticSearch(message_history)
    related_content = semantic_search.semantic_search(input_string)
    return related_content


def reformat_nested_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list


def chatbot_with_memory(num_messages=1, token_window_size=100, long_term_memory=False):
    if long_term_memory:
        with open("data/combined_data.json", "r") as f:
            previous_messages = json.load(f)

        full_message_history = previous_messages
        joined_full_message_history = " ".join(
            [message["content"] for message in full_message_history]
        )
        user_input = input("Enter your message: ")
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

        user_input = input("Enter your message: ")
        message_history = chat_gpt(user_input, full_context)
        full_message_history.append(message_history)

    return full_message_history
