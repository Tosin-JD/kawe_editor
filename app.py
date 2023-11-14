"""app.py
    this contains the main loop for the application
"""

import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle

import pytesseract
from PIL import Image
from tkinterdnd2 import TkinterDnD, DND_FILES
import configparser

from textblob import Word
import re
import nltk

from components.find import FindWindow, ReplaceWindow
from components.menu import TextEditorMenu, MainMenu
from components.tabs import HomeTab, ConvertTab  
from components.spellchecker import SpellcheckText
import os

class TextEditor(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        self.geometry("800x600")

        # Create a themed style
        self.style = ThemedStyle(self)
        self.style.set_theme("radiance")

        self.current_file = None
        self.word_wrap = False  # Initially, word wrap is disabled.
        
        # configure the the weight and column
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Create the Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var)
        self.status_bar.grid(column=0, row=3, sticky="e")

        # Create the Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=0, row=0, columnspan=2, sticky="ew")
        
        # Create a Text widget for text editing in the Home tab
        # self.text = tk.Text(self, wrap=tk.WORD)
        self.text = SpellcheckText(self, wrap=tk.WORD)
        self.text.grid(column=0, row=1, sticky="nsew")
        
        self.vertical_scrolbar = ttk.Scrollbar(self, orient="vertical")
        self.vertical_scrolbar.grid(column=1, row=1, sticky="ns")
        self.vertical_scrolbar.config(command=self.text.yview)
        
        self.horizontal_scrolbar = ttk.Scrollbar(self, orient="horizontal")
        self.horizontal_scrolbar.grid(column=0, row=2, sticky="ew")
        self.horizontal_scrolbar.config(command=self.text.xview)
        
        # Create a menu bar
        self.menu = MainMenu(self)
        self.config(menu=self.menu)

        # Create the Home tab
        self.create_tab(HomeTab, "Home")
        self.create_tab(ConvertTab, "Image To Text")
        
        # Initial word count
        self.update_status()
        self.load_last_opened_file()
        self.bind("<Key>", self.update_status)
        self.text.bind("<B1-Motion>", self.update_status)
        self.text.drop_target_register(DND_FILES)
        self.text.dnd_bind('<<Drop>>', self.drop)
        self.protocol("WM_DELETE_WINDOW", self.exit_app)
        
    def correct_words(self):
        selected_text = self.get_selected_text()
        if selected_text:
            words = selected_text.split()
            words = [word for word in words]
            words = [re.sub(r'[^A-Za-z0-9]+', '', word) for word in words]

            corrected_text = ""
            for word in words:
                corrected_word = Word(word).spellcheck()[0][0]
                corrected_text += corrected_word + " "

            corrected_text = corrected_text.strip()

            result = str.replace(str(self.text.get("1.0", "end-1c")), 
                                 selected_text, corrected_text)
            self.text.delete("1.0", "end-1c")
            self.text.insert("1.0", result)
            self.update_status()
        
    def load_last_opened_file(self):
        config = configparser.ConfigParser()
        config_file_path = os.path.expanduser("~/.text_editor_config.ini")

        if os.path.exists(config_file_path):
            config.read(config_file_path)
            last_file = config.get("Settings", "last_file", fallback=None)

            if last_file and os.path.isfile(last_file):
                with open(last_file, "r") as file:
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, file.read())
                self.current_file = last_file
                self.update_status()
                self.save_last_opened_file()
                
    def save_last_opened_file(self):
        config = configparser.ConfigParser()
        config_file_path = os.path.expanduser("~/.text_editor_config.ini")

        config["Settings"] = {"last_file": str(self.current_file)}

        with open(config_file_path, "w") as configfile:
            config.write(configfile)
            
    def get_selected_text(self):
        if self.text.tag_ranges(tk.SEL):
            selected_text = self.text.selection_get()
        else:
            selected_text = self.text.get("1.0", "end-1c")
        return selected_text
            
    def copy_text(self):
        selected_text = self.get_selected_text()
        if selected_text:
            self.clipboard_clear()
            self.clipboard_append(selected_text)
            self.update_idletasks()
        
    def create_tab(self, tab_class, tab_text):
        tab_frame = tab_class(self)
        self.notebook.add(tab_frame, text=tab_text)
        
        if tab_text == "Home":
            self.notebook.select(tab_frame)
            
    def convert_image_to_text(self):
        file_paths = filedialog.askopenfilenames(defaultextension=".png", filetypes=[("Image Files", ".png .jpg")], multiple=True)
        if file_paths:
            try:
                self.convert(file_paths)
                # Clear the current file path after converting from all images
                self.current_file = None
                self.update_status()
            except Exception as e:
                print(f"Error converting image to text: {e}")

    def drop(self, event):
        # Delete entire existing content
        self.text.delete("1.0", "end")

        # Check if the dropped data is text
        if event.data.startswith("text/plain"):
            dropped_text = event.data
            # Get the current cursor position
            cursor_pos = self.text.index(tk.INSERT)
            # Insert the dropped text at the cursor position
            self.text.insert(cursor_pos, dropped_text)

        # Check if the dropped file has a ".txt" extension
        elif event.data.endswith(".txt"):
            with open(event.data, "r") as f:
                # Read content line by line and insert into the textbox
                for text_line in f:
                    text_line = text_line.strip()
                    self.text.insert("end", f"{text_line}\n")

        # Check if the dropped file is an image
        elif event.data.endswith((".png", ".jpg", ".jpeg")):
            try:
                self.convert([event.data])
                # Clear the current file path after converting from the image
                self.current_file = None
                self.update_status()
            except Exception as e:
                print(f"Error converting image to text: {e}")

    def convert(self, file_paths):
        # Set the path to the Tesseract executable based on the operating system
        if os.name == 'posix':  # Linux or macOS
            pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update if necessary
        elif os.name == 'nt':  # Windows
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update if necessary

        for file_path in file_paths:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)

            # Add the text from the current image to the text box
            self.text.insert(tk.END, text)
            self.text.insert(tk.END, "\n")

    def update_status(self, event=None):
        text_content = self.text.get(1.0, tk.END)
        total_words = self.count_words(text_content)

        if self.text.tag_ranges(tk.SEL):
            sel_start, sel_end = self.text.tag_ranges(tk.SEL)
            selected_text = self.text.get(sel_start, sel_end)
            selected_words = self.count_words(selected_text)
        else:
            selected_words = 0

        self.status_var.set(f"{selected_words}/{total_words} words")
    
    def count_words(self, text):
        # Use a more accurate word counting method
        words = text.split()
        return len(words)
    
    def exit_app(self):
        self.save_last_opened_file()
        self.destroy()

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end")
        self.update_status()

    def toggle_word_wrap(self):
        self.word_wrap = not self.word_wrap
        wrap_setting = tk.WORD if self.word_wrap else tk.NONE
        self.text.config(wrap=wrap_setting)
        self.update_status()
        
    def cntrlf(self):
        self.find()
    
    def find(self):
        window = FindWindow(self)
        window.grab_set()
        
    def replace(self):
        window = ReplaceWindow(self)
        window.grab_set()
    
if __name__ == "__main__":
    editor = TextEditor()
    editor.mainloop()
