
# Python program to create a basic GUI
# application using the customtkinter module

import customtkinter as ctk
import tkinter as tk

# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System")

# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green")

# App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GUI Application")
		
		# Text Box
        self.displayBox = ctk.CTkTextbox(self, width=1000,
										height=400)
        self.displayBox.grid(row=0, column=0, columnspan=4,
							padx=20, pady=20, sticky="nsew")

		# Name Entry Field
        self.nameEntry = ctk.CTkEntry(self,
						placeholder_text="Teja")
        self.nameEntry.grid(row=5, column=0,
							columnspan=3, padx=20,
							pady=20, sticky="ew")
		
        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self,
										text="Generate Results")
        self.generateResultsButton.grid(row=5, column=3,
										columnspan=2,
										padx=20, pady=20,
										sticky="ew")
    def generateResults(self):
        self.displayBox.delete("0.0", "200.0")
        text = self.createText()
        self.displayBox.insert("0.0", text)
	 
    def createText(self):
         text = "Hello, " + self.nameEntry.get()
         return text


if __name__ == "__main__":
	app = App()
	app.mainloop()
