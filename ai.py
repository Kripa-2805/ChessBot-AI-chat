

import tkinter as tk
from tkinter import scrolledtext
import os
import sys

# Install google-generativeai if not installed
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    print("google-generativeai not found. Installing now...")
    os.system(f"{sys.executable} -m pip install google-generativeai")
    import google.generativeai as genai # Try importing again after installation

# Set up Gemini API key
GENAI_API_KEY = "Your API key"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

class ChatbotGUIai:
    def __init__(self, master):
        #self.master = master
        #self.master.title("AI Chatbot (Gemini)")
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.chat_display.config(state=tk.DISABLED)

        # User input field
        self.user_input = tk.Entry(master, width=40,font=("Verdana", 12))
        self.user_input.grid(row=1, column=0, padx=5, pady=5)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=0, pady=5)

    def send_message(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message(f"You: {user_text}\n")
        self.user_input.delete(0, tk.END)

        # Get AI response
        ai_response = self.get_ai_response(user_text)
        self.display_message(f"AI: {ai_response}\n")

    def get_ai_response(self, prompt):
        try:
            
            model = genai.GenerativeModel("models/gemini-2.5-pro")
            
            response = model.generate_content(prompt)

            # Correctly extract AI response
            if response and hasattr(response, "text"):
                return response.text.strip()
            elif hasattr(response, "candidates") and response.candidates:
                return response.candidates[0].content.parts[0].text.strip()
            else:
                return "I'm sorry, I couldn't generate a response."

        except Exception as e:
            print(f"Error: {e}")  # Print the actual error in the console
            return "An error occurred. Please check your API key and internet connection."

            
    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

