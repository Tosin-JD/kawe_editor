"""
components.menu
"""

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, relief="flat")
        self.master = master
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_help_menu()

    def create_file_menu(self):
        self.file_menu = tk.Menu(self, relief="flat")
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.exit_app) 

    def create_edit_menu(self):
        self.edit_menu = tk.Menu(self, relief="flat")
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Select All", command=self.master.select_all, accelerator="Ctrl+A")
        self.edit_menu.add_command(label="Find", command=self.master.find, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Find and Replace", command=self.master.replace, accelerator="Ctrl+H")
        
    def create_view_menu(self):
        self.view_menu = tk.Menu(self, relief="flat")
        self.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label="Word Wrap", command=self.master.toggle_word_wrap, accelerator="Ctrl+W")
        
        self.theme_menu = tk.Menu(self.view_menu, relief="flat")
        self.view_menu.add_cascade(label="Theme", menu=self.theme_menu)

        # Adding menu items for each theme
        self.theme_menu.add_command(label="Radiance", command=lambda: self.master.style.set_theme('radiance'))
        self.theme_menu.add_command(label="Blue", command=lambda: self.master.style.set_theme('blue'))
        self.theme_menu.add_command(label="ScidBlue", command=lambda: self.master.style.set_theme('scidblue'))
        self.theme_menu.add_command(label="Plastic", command=lambda: self.master.style.set_theme('plastik'))
        self.theme_menu.add_command(label="Arc", command=lambda: self.master.style.set_theme('arc'))
        
    def create_help_menu(self):
        help_menu = tk.Menu(self, tearoff=0, relief="flat")  
        help_menu.add_command(label="About", command=self.master.toggle_word_wrap)  
        help_menu.add_command(label="Get Started", command=self.master.toggle_word_wrap)  
        help_menu.add_command(label="How To...", command=self.master.toggle_word_wrap)  
        self.add_cascade(label="Help", menu=help_menu) 
        
    def new_file(self):
        self.master.current_file = None
        self.master.text.delete(1.0, tk.END)
        self.master.update_status()
        
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.master.text.delete(1.0, tk.END)
                self.master.text.insert(tk.END, file.read())
            self.master.current_file = file_path
            self.master.save_last_opened_file()
            self.master.update_status()

    def save_file(self):
        if self.master.current_file:
            with open(self.master.current_file, "w") as file:
                file.write(self.master.text.get(1.0, tk.END))
            self.master.save_last_opened_file()
            self.master.update_status()
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.master.text.get(1.0, tk.END))
            self.master.current_file = file_path
            self.master.save_last_opened_file()
            self.master.update_status()

 
