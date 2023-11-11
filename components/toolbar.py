import tkinter as tk
from tkinter import ttk

class Toolbar:
    def __init__(self, parent, text_editor):
        self.parent = parent
        self.text_editor = text_editor
        self.toolbar_frame = ttk.Frame(parent)
        self.toolbar_frame.pack(fill=tk.BOTH)

        new_button = ttk.Button(self.toolbar_frame, text="New", command=self.text_editor.new_file)
        open_button = ttk.Button(self.toolbar_frame, text="Open", command=self.text_editor.open_file)
        save_button = ttk.Button(self.toolbar_frame, text="Save", command=self.text_editor.save_file)

        new_button.grid(row=0, column=0)
        open_button.grid(row=0, column=1)
        save_button.grid(row=0, column=2)
        self.toolbar_frame.rowconfigure(0, weight=0)
