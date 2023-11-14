# tabs.py

import tkinter as tk
from tkinter import ttk

class HomeTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        
        home_toolbar = ttk.Frame(self)
        home_toolbar.pack(fill=tk.BOTH)
        
        new_button = ttk.Button(home_toolbar, text="New", command=parent.menu.new_file)
        open_button = ttk.Button(home_toolbar, text="Open", command=parent.menu.open_file)
        save_button = ttk.Button(home_toolbar, text="Save", command=parent.menu.save_file)

        new_button.grid(row=0, column=0)
        open_button.grid(row=0, column=1)
        save_button.grid(row=0, column=2)
        home_toolbar.rowconfigure(0, weight=0)

class ConvertTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        convert_toolbar = ttk.Frame(self)
        convert_toolbar.pack(fill=tk.BOTH)

        itt_button = ttk.Button(convert_toolbar, text="Convert Scanned Images", 
                                command=parent.convert_image_to_text)
        correct_word_button = ttk.Button(convert_toolbar, text="Correct Words", 
                                         command=parent.correct_words)
        # correct_sentence_button = ttk.Button(convert_toolbar, text="Correct Sentences", 
        #                                      command=parent.correct_sentences)
        copy_button = ttk.Button(convert_toolbar, text="Copy Text",
                                 command=parent.copy_text)

        itt_button.grid(row=0, column=0, ipadx=5)
        correct_word_button.grid(row=0, column=1, ipadx=5)
        # correct_sentence_button.grid(row=0, column=2, ipadx=5)
        copy_button.grid(row=0, column=2, ipadx=5)
        convert_toolbar.rowconfigure(0, weight=0)
