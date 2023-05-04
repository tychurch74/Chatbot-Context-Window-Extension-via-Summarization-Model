import openai

from modules.text_summarization import iterative_summary
from modules.semantic_search import SemanticSearch

MODEL = "gpt-3.5-turbo"

def chat_gpt(user_input, context="no conversation history yet"):
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
        
    generated_message = response['choices'][0]['message']
    generated_message_data = {
        "role": generated_message['role'],
        "content": "assistant said: " + generated_message['content']
    }
        
    message_history.append(user_message)
    message_history.append(generated_message_data)
    print(generated_message['content'])

    return message_history

def semantic_search(message_history, input_string):
    semantic_search = SemanticSearch(message_history)
    related_content = semantic_search.semantic_search(input_string)
    return related_content


def chatbot_with_memory(num_messages=3, token_window_size=100):
    user_input = input("Enter your message: ")
    message_history = chat_gpt(user_input)
    for i in range(0,num_messages):
        joined_message_history = " ".join([message['content'] for message in message_history])
        context = iterative_summary(joined_message_history, token_window_size)
        related_content = semantic_search(joined_message_history, user_input)
        full_context = related_content + context
        user_input = input("Enter your message: ")
        message_history = chat_gpt(user_input, full_context)

    return message_history

