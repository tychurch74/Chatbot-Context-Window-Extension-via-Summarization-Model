# Python program to create a basic GUI
# application using the customtkinter module

import customtkinter as ctk
import tkinter as tk
import os
from tkinter import Tk, Text, Entry, Button, Scrollbar, END, font
from modules.chatGPT import ChatGPT


# Settings
openai_api_key = os.environ["OPENAI_API_KEY"]
enable_json_output = False
text_to_speech_enabled = False
chunk_size = 4
completion_file_path = "testing_data/test-1_completion.json"
message_history_file_path = "testing_data/test-5_message_history.json"

chat_gpt = ChatGPT(
    openai_api_key,
    enable_json_output=enable_json_output,
    chunk_size=chunk_size,
    completion_file_path=completion_file_path,
)

# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System")

# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("dark-blue")


# App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        message_font = ctk.CTkFont(family="Helvetica", size=18)
        prompt_font = ctk.CTkFont(family="Helvetica", size=14)
        self.title("GUI Application")

        # Text Box
        self.displayBox = ctk.CTkTextbox(
            self, width=1000, height=400, wrap="word", font=message_font
        )
        self.displayBox.grid(
            row=0, column=0, columnspan=4, padx=20, pady=20, sticky="nsew"
        )

        # Name Entry Field
        self.nameEntry = ctk.CTkEntry(
            self,
            placeholder_text="Type your message here...",
            font=prompt_font,
            height=32,
        )
        self.nameEntry.grid(
            row=5, column=0, columnspan=3, padx=20, pady=20, sticky="ew"
        )

        # Generate Button
        self.generateResultsButton = ctk.CTkButton(
            self, text="Send", command=self.generateResults
        )
        self.generateResultsButton.grid(
            row=5, column=3, columnspan=2, padx=20, pady=20, sticky="ew"
        )

    def generateResults(self):
        user_text = self.createText()
        user_message = "You -> " + user_text
        self.displayBox.insert(END, user_message)
        chat_response = chat_gpt.chat(user_text)
        self.displayBox.insert(END, "\n")
        self.displayBox.insert(END, "\n")
        self.displayBox.insert(END, f"Bot -> {chat_response}")
        self.displayBox.insert(END, "\n")

    def createText(self):
        text = self.nameEntry.get()
        return text


if __name__ == "__main__":
    app = App()
    app.mainloop()
