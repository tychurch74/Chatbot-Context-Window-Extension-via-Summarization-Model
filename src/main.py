import openai
import os
from modules.text_summarization import Summarizer
from data.io_utils import write_json, json_obj, add_to_json, read_json

# Settings
openai.api_key = os.environ["OPENAI_API_KEY"]
enable_json_output = False
num_iterations = 3
chunk_size = 4
completion_file_path = "completion.json"
message_history_file_path = "message_history.json"

message_history = []

def generate_conversation_summary(message_history):
    if not message_history:
        conversation_summary = [{"role": "system", "content": "You are a chatbot that gives short, concise responses based on the following context (no conversation history yet)"}]
    else:
        content = [message["content"] for message in message_history]
        combined_content = "".join(content)
        summarizer = Summarizer()
        summary = summarizer.process_in_chunks(combined_content, chunk_size=chunk_size)
        conversation_summary = [{"role": "system", "content": f"You are a chatbot that gives short, concise responses based on the following context {summary}"}]

    return conversation_summary

def log_to_json(data, file_path):
    if enable_json_output:
        add_to_json(data, file_path)

def chat(inp, role="user"):
    conversation_summary = generate_conversation_summary(message_history)
    conversation_summary.append({"role": role, "content": inp})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_summary
    )
    chat_data = json_obj(conversation_summary, completion)
    log_to_json(chat_data, completion_file_path)
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": reply_content})
    return reply_content

def main():
    for i in range(num_iterations):
        user_input = input("> ")
        print("User's input was:", user_input)
        print(chat(user_input))
        print()

    conversation_summary = generate_conversation_summary(message_history)
    data = json_obj(message_history, conversation_summary)
    write_json(data, message_history_file_path)

if __name__ == "__main__":
    main()
