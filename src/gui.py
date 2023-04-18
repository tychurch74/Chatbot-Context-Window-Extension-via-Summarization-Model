import os
import tkinter as tk

from tkinter import Tk, Text, Entry, Button, Scrollbar, END, font

from modules.chatGPT import ChatGPT


# Settings
openai_api_key = os.environ["OPENAI_API_KEY"]
enable_json_output = False
num_iterations = 2
chunk_size = 4
completion_file_path = "testing_data/test-1_completion.json"
message_history_file_path = "testing_data/test-5_message_history.json"
    
chat_gpt = ChatGPT(openai_api_key, enable_json_output=enable_json_output, chunk_size=chunk_size, completion_file_path=completion_file_path)    

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
            chat_history.insert(END, "\n" + f"Bot -> {chat_gpt.chat(user_input)}")
            chat_history.insert(END, "\n")

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

