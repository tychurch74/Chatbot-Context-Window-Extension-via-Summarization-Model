import openai
import json

from modules.text_summarization import Summarizer
from data.io_utils import write_json, json_obj, add_to_json

openai.api_key = "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"
                                
message_history = []

def conversation_sum(message_history):
    if not message_history:
        conversation_summary = [{"role": "system", "content": "You are a chatbot that gives short, concise responses based on the following context (no conversation history yet)"}]
        
    else:
        content = [message["content"] for message in message_history]
        combined_content = "".join(content)

        summarizer = Summarizer()
        corrected = summarizer.process_in_chunks(combined_content, chunk_size=4)

        conversation_summary = [{"role": "system", "content": f"You are a chatbot that gives short, concise responses based on the following context {corrected}"}]

    return(conversation_summary)


def chat(inp, role="user"):
    #message_history.append({"role": role, "content": f"{inp}"})
    conversation_summary = conversation_sum(message_history)
    conversation_summary.append({"role": role, "content": f"{inp}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_summary
    )
    chat_data = json_obj(conversation_summary, completion)
    add_to_json(chat_data, "completion.json") 
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    return reply_content


for i in range(3):
    user_input = input("> ")
    print("User's input was: ", user_input)
    print(chat(user_input))
    print()

con_sum = conversation_sum(message_history)
data = json_obj(message_history, con_sum)
write_json(data, "message_history.json")


