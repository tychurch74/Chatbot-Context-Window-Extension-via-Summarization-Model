import customtkinter as ctk
import tkinter as tk
import openai
import os

from tkinter import ttk
from modules.text_summarization import Summarizer

# Settings
openai.api_key = os.environ["OPENAI_API_KEY"]
enable_json_output = True
num_iterations = 5
chunk_size = 4
completion_file_path = "testing_data/test-1_completion.json"
message_history_file_path = "testing_data/test-4_message_history.json"

message_history = []


def generate_conversation_summary(message_history):
    if not message_history:
        conversation_summary = [
            {
                "role": "system",
                "content": "You are a chatbot that gives short, concise responses based on the following context: (no conversation history yet)",
            }
        ]
    else:
        content = [message["content"] for message in message_history]
        combined_content = "".join(content)
        summarizer = Summarizer()
        summary = summarizer.process_in_chunks(combined_content, chunk_size=chunk_size)
        conversation_summary = [
            {
                "role": "system",
                "content": f"You are a chatbot that gives short, concise responses based on the following context: {summary}",
            }
        ]

    return conversation_summary


def chat(inp, role="user"):
    conversation_summary = generate_conversation_summary(message_history)
    conversation_summary.append(
        {"role": role, "content": f"based on the context given {inp}"}
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation_summary
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": reply_content})
    return reply_content


def main(input_value, input_text, output_text):
    input_text = input_text.get("1.0", tk.END).strip()
    if input_value == 1:
        reply = chat(input_text)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, reply)


def create_gui():
    window = tk.Tk()
    window.title("Infinite Chatbot")
    window.geometry("700x500")

    def on_button_click(input_value):
        main(input_value, input_text, output_text)

    input_label = ttk.Label(window, text="Input")
    input_label.pack(pady=(10, 5))

    input_text = tk.Text(window, font="arial", wrap=tk.WORD, width=60, height=10)
    input_text.pack(pady=(0, 5))

    btn1 = ctk.CTkButton(
        window, text="Submit", command=lambda: on_button_click(1), corner_radius=10
    )
    btn1.pack(pady=5)

    output_label = ttk.Label(window, text="Output")
    output_label.pack(pady=(10, 5))

    output_text = tk.Text(window, font="arial", wrap=tk.WORD, width=60, height=10)
    output_text.pack(pady=(0, 5))

    window.mainloop()


if __name__ == "__main__":
    create_gui()
