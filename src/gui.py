import openai
import os
import tkinter as tk

from tkinter import Tk, Text, Entry, Button, Scrollbar, END, font
from modules.text_summarization import Summarizer


# Settings
openai.api_key = os.environ["OPENAI_API_KEY"]
enable_json_output = False
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


# GUI
def create_chatbot_gui():
    root = Tk()
    root.title("Chatbot")
    root.geometry("700x600")
    root.config(bg="#2C3E50")

    BACKGROUND_GRAY = "#ABB2B9"
    BACKGROUND_COLOR = "#17202A"
    TEXT_COLOR = "#EAECEE"
    FONT_STANDARD = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"

    custom_font = font.Font(family="Helvetica", size=14)

    def send_message():
        user_message = "You -> " + message_entry.get()
        chat_history.insert(END, "\n" + user_message)

        user_input = message_entry.get().lower()

        if user_input == "hello":
            chat_history.insert(END, "\n" + "Bot -> Hi there, how can I help?")
        else:
            chat_history.insert(END, "\n")
            chat_history.insert(END, "\n" + f"Bot -> {chat(user_input)}")

        message_entry.delete(0, END)

    chat_history = Text(root, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=custom_font, width=60, wrap=tk.WORD, padx=10, pady=10)
    chat_history.grid(row=1, column=0, columnspan=2, padx=(10, 0), pady=(10, 0))

    chat_scrollbar = Scrollbar(chat_history, bg=BACKGROUND_GRAY)
    chat_scrollbar.place(relheight=1, relx=0.975)

    message_entry = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=custom_font, width=55)
    message_entry.grid(row=2, column=0, padx=(10, 0), pady=(0, 10))

    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BACKGROUND_GRAY, command=send_message)
    send_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    create_chatbot_gui()

